import io
import sys

import pytest
import torch

from guessme.model.preprocess import CANVAS_SIZE, canvas_to_tensor, print_ascii


def test_canvas_to_tensor():
    """Canvas points -> (1, 28, 28) tensor"""
    points = [{"x": 14, "y": 14}, {"x": 15, "y": 15}]  # simple stroke
    tensor = canvas_to_tensor(points)
    assert tensor.shape == (1, 28, 28)


def test_canvas_to_tensor_normalized():
    """Output values should be normalized (0-1 range)"""
    points = [{"x": 14, "y": 14}]
    tensor = canvas_to_tensor(points)
    assert tensor.min() == 0.0
    assert tensor.max() <= 1.0


# === Scaling tests ===


class TestCanvasScaling:
    """Test that canvas coords (0-400) scale correctly to tensor coords (0-27)"""

    def test_scale_origin(self):
        """Canvas (0,0) -> tensor [0,0]"""
        points = [{"x": 0, "y": 0}]
        tensor = canvas_to_tensor(points)
        assert tensor[0, 0, 0] == 1.0

    def test_scale_max(self):
        """Canvas (400,400) -> tensor [27,27]"""
        points = [{"x": 400, "y": 400}]
        tensor = canvas_to_tensor(points)
        assert tensor[0, 27, 27] == 1.0

    def test_scale_center(self):
        """Canvas (200,200) -> tensor ~[13,13]"""
        points = [{"x": 200, "y": 200}]
        tensor = canvas_to_tensor(points)
        expected_idx = int(200 * 27 / CANVAS_SIZE)  # = 13
        assert tensor[0, expected_idx, expected_idx] == 1.0

    def test_scale_quarter(self):
        """Canvas (100,100) -> tensor ~[6,6]"""
        points = [{"x": 100, "y": 100}]
        tensor = canvas_to_tensor(points)
        expected_idx = int(100 * 27 / CANVAS_SIZE)  # = 6
        assert tensor[0, expected_idx, expected_idx] == 1.0

    def test_scale_three_quarter(self):
        """Canvas (300,300) -> tensor ~[20,20]"""
        points = [{"x": 300, "y": 300}]
        tensor = canvas_to_tensor(points)
        expected_idx = int(300 * 27 / CANVAS_SIZE)  # = 20
        assert tensor[0, expected_idx, expected_idx] == 1.0

    @pytest.mark.parametrize(
        "canvas_x,canvas_y,expected_x,expected_y",
        [
            (0, 0, 0, 0),
            (100, 100, 6, 6),
            (200, 200, 13, 13),
            (300, 300, 20, 20),
            (400, 400, 27, 27),
            (50, 150, 3, 10),
            (350, 250, 23, 16),
        ],
    )
    def test_scale_parametrized(self, canvas_x, canvas_y, expected_x, expected_y):
        """Parametrized scaling tests for various coords"""
        points = [{"x": canvas_x, "y": canvas_y}]
        tensor = canvas_to_tensor(points)
        # tensor is [channel, y, x] so check [0, expected_y, expected_x]
        assert tensor[0, expected_y, expected_x] == 1.0

    def test_no_modulo_wrap(self):
        """Ensure coords don't wrap with modulo (the bug we fixed)"""
        # With old modulo bug: x=200 % 28 = 4, y=200 % 28 = 4
        # With correct scaling: x=200*27/400 = 13, y=13
        points = [{"x": 200, "y": 200}]
        tensor = canvas_to_tensor(points)

        # Should NOT be at (4,4) - that was the bug
        assert tensor[0, 4, 4] == 0.0

        # Should be at (13,13)
        assert tensor[0, 13, 13] == 1.0

    def test_clamp_out_of_bounds(self):
        """Coords outside 0-400 should clamp to valid range"""
        points = [{"x": -50, "y": -50}, {"x": 500, "y": 500}]
        tensor = canvas_to_tensor(points)
        # Should clamp to edges without error
        assert tensor[0, 0, 0] == 1.0  # negative clamped to 0
        assert tensor[0, 27, 27] == 1.0  # >400 clamped to 27


# === print_ascii tests ===


class TestPrintAscii:
    """Test ASCII visualization of tensors"""

    def test_print_ascii_blank(self):
        """Blank tensor prints 28 lines of 28 spaces each"""
        tensor = torch.zeros(1, 28, 28)
        captured = io.StringIO()
        sys.stdout = captured
        print_ascii(tensor)
        sys.stdout = sys.__stdout__

        output = captured.getvalue()
        # Split without strip - blank lines have 28 spaces
        lines = output.split("\n")
        # Should have 28 content lines + 1 empty line from final print()
        assert len(lines) >= 28
        # First 28 lines should be 28 spaces each
        for i in range(28):
            assert lines[i] == " " * 28

    def test_print_ascii_full(self):
        """Full tensor prints all @ chars"""
        tensor = torch.ones(1, 28, 28)
        captured = io.StringIO()
        sys.stdout = captured
        print_ascii(tensor)
        sys.stdout = sys.__stdout__

        output = captured.getvalue()
        lines = output.split("\n")
        assert len(lines) >= 28
        # All chars should be @ (last char in " .:-=+*#%@")
        for i in range(28):
            assert lines[i] == "@" * 28

    def test_print_ascii_single_pixel(self):
        """Single pixel at known location"""
        tensor = torch.zeros(1, 28, 28)
        tensor[0, 5, 10] = 1.0  # row 5, col 10

        captured = io.StringIO()
        sys.stdout = captured
        print_ascii(tensor)
        sys.stdout = sys.__stdout__

        output = captured.getvalue()
        lines = output.split("\n")

        # Row 5 should have @ at position 10
        assert lines[5][10] == "@"
        # Other positions in row 5 should be space
        assert lines[5][0] == " "
        assert lines[5][27] == " "

    def test_print_ascii_gradient(self):
        """Mid-value pixels use middle chars"""
        tensor = torch.zeros(1, 28, 28)
        tensor[0, 0, 0] = 0.5  # Mid brightness

        captured = io.StringIO()
        sys.stdout = captured
        print_ascii(tensor)
        sys.stdout = sys.__stdout__

        output = captured.getvalue()
        # 0.5 * 9 = 4.5 -> idx 4 -> char '+'
        assert output[0] in "=+"  # chars at idx 4-5


# === Debug mode test ===


def test_canvas_to_tensor_debug_mode():
    """Debug mode should print ASCII output"""
    points = [{"x": 200, "y": 200}]

    captured = io.StringIO()
    sys.stdout = captured
    canvas_to_tensor(points, debug=True)
    sys.stdout = sys.__stdout__

    output = captured.getvalue()
    # Should have printed something (28 lines of ASCII + empty line)
    assert len(output) > 0
    lines = output.split("\n")
    assert len(lines) >= 28
