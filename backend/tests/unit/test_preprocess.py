import io
import sys

import pytest
import torch

from guessme.model.preprocess import (
    CANVAS_SIZE,
    bresenham_line,
    canvas_to_tensor,
    center_of_mass,
    center_tensor,
    dilate_strokes,
    draw_lines_on_tensor,
    gaussian_blur,
    gaussian_kernel,
    print_ascii,
    tensor_to_ascii,
)


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
    """Test that canvas coords (0-400) scale correctly to tensor coords (0-27)

    Note: These tests disable preprocessing to test raw scaling.
    """

    def test_scale_origin(self):
        """Canvas (0,0) -> tensor [0,0]"""
        points = [{"x": 0, "y": 0}]
        tensor = canvas_to_tensor(points, dilate=False, center=False, blur=False)
        assert tensor[0, 0, 0] == 1.0

    def test_scale_max(self):
        """Canvas (400,400) -> tensor [27,27]"""
        points = [{"x": 400, "y": 400}]
        tensor = canvas_to_tensor(points, dilate=False, center=False, blur=False)
        assert tensor[0, 27, 27] == 1.0

    def test_scale_center(self):
        """Canvas (200,200) -> tensor ~[13,13]"""
        points = [{"x": 200, "y": 200}]
        tensor = canvas_to_tensor(points, dilate=False, center=False, blur=False)
        expected_idx = int(200 * 27 / CANVAS_SIZE)  # = 13
        assert tensor[0, expected_idx, expected_idx] == 1.0

    def test_scale_quarter(self):
        """Canvas (100,100) -> tensor ~[6,6]"""
        points = [{"x": 100, "y": 100}]
        tensor = canvas_to_tensor(points, dilate=False, center=False, blur=False)
        expected_idx = int(100 * 27 / CANVAS_SIZE)  # = 6
        assert tensor[0, expected_idx, expected_idx] == 1.0

    def test_scale_three_quarter(self):
        """Canvas (300,300) -> tensor ~[20,20]"""
        points = [{"x": 300, "y": 300}]
        tensor = canvas_to_tensor(points, dilate=False, center=False, blur=False)
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
        tensor = canvas_to_tensor(points, dilate=False, center=False, blur=False)
        # tensor is [channel, y, x] so check [0, expected_y, expected_x]
        assert tensor[0, expected_y, expected_x] == 1.0

    def test_no_modulo_wrap(self):
        """Ensure coords don't wrap with modulo (the bug we fixed)"""
        # With old modulo bug: x=200 % 28 = 4, y=200 % 28 = 4
        # With correct scaling: x=200*27/400 = 13, y=13
        points = [{"x": 200, "y": 200}]
        tensor = canvas_to_tensor(points, dilate=False, center=False, blur=False)

        # Should NOT be at (4,4) - that was the bug
        assert tensor[0, 4, 4] == 0.0

        # Should be at (13,13)
        assert tensor[0, 13, 13] == 1.0

    def test_clamp_out_of_bounds(self):
        """Coords outside 0-400 should clamp to valid range"""
        points = [{"x": -50, "y": -50}, {"x": 500, "y": 500}]
        tensor = canvas_to_tensor(points, dilate=False, center=False, blur=False)
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


# === tensor_to_ascii tests ===


def test_tensor_to_ascii_returns_string():
    """tensor_to_ascii returns string with 28 lines"""
    tensor = torch.zeros(1, 28, 28)
    tensor[0, 10, 10] = 1.0

    result = tensor_to_ascii(tensor)

    assert isinstance(result, str)
    lines = result.split("\n")
    assert len(lines) == 28
    assert "@" in lines[10]  # Row 10 has the pixel


def test_tensor_to_ascii_full():
    """Full tensor returns all @ chars"""
    tensor = torch.ones(1, 28, 28)
    result = tensor_to_ascii(tensor)

    lines = result.split("\n")
    for line in lines:
        assert line == "@" * 28


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


# === Bresenham Line Tests ===


class TestBresenhamLine:
    """Test Bresenham line drawing algorithm"""

    def test_horizontal_line(self):
        """Horizontal line from (0,0) to (5,0)"""
        points = bresenham_line(0, 0, 5, 0)
        assert points == [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)]

    def test_vertical_line(self):
        """Vertical line from (0,0) to (0,5)"""
        points = bresenham_line(0, 0, 0, 5)
        assert points == [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]

    def test_diagonal_line(self):
        """Diagonal line from (0,0) to (3,3)"""
        points = bresenham_line(0, 0, 3, 3)
        assert len(points) == 4
        assert points[0] == (0, 0)
        assert points[-1] == (3, 3)

    def test_single_point(self):
        """Single point when start equals end"""
        points = bresenham_line(5, 5, 5, 5)
        assert points == [(5, 5)]

    def test_reverse_direction(self):
        """Line from (5,0) to (0,0)"""
        points = bresenham_line(5, 0, 0, 0)
        assert len(points) == 6
        assert points[0] == (5, 0)
        assert points[-1] == (0, 0)

    def test_steep_line(self):
        """Steep line (dy > dx)"""
        points = bresenham_line(0, 0, 2, 5)
        assert points[0] == (0, 0)
        assert points[-1] == (2, 5)
        # Should have continuous y values
        y_values = [p[1] for p in points]
        for i in range(len(y_values) - 1):
            assert y_values[i + 1] - y_values[i] <= 1


# === Draw Lines Tests ===


class TestDrawLines:
    """Test drawing connected lines on tensor"""

    def test_connects_distant_points(self):
        """Lines should connect distant points"""
        img = torch.zeros(28, 28)
        scaled_points = [(0, 0), (10, 0)]  # Horizontal gap
        draw_lines_on_tensor(img, scaled_points)

        # All points from 0 to 10 should be filled
        for x in range(11):
            assert img[0, x] == 1.0

    def test_diagonal_connection(self):
        """Diagonal lines should be continuous"""
        img = torch.zeros(28, 28)
        scaled_points = [(0, 0), (5, 5)]
        draw_lines_on_tensor(img, scaled_points)

        # Start and end should be filled
        assert img[0, 0] == 1.0
        assert img[5, 5] == 1.0

    def test_single_point_no_line(self):
        """Single point should not draw line"""
        img = torch.zeros(28, 28)
        scaled_points = [(5, 5)]
        draw_lines_on_tensor(img, scaled_points)
        # Function doesn't draw individual points, just lines
        assert img.sum() == 0

    def test_multiple_segments(self):
        """Multiple line segments"""
        img = torch.zeros(28, 28)
        scaled_points = [(0, 0), (5, 0), (5, 5)]
        draw_lines_on_tensor(img, scaled_points)

        # Horizontal segment
        assert img[0, 0] == 1.0
        assert img[0, 5] == 1.0
        # Vertical segment
        assert img[5, 5] == 1.0


# === Dilation Tests ===


class TestDilateStrokes:
    """Test stroke dilation"""

    def test_single_pixel_expands(self):
        """Single pixel should expand to 3x3"""
        tensor = torch.zeros(1, 28, 28)
        tensor[0, 14, 14] = 1.0

        dilated = dilate_strokes(tensor)

        # Center pixel should still be 1
        assert dilated[0, 14, 14] == 1.0
        # Neighbors should also be 1
        assert dilated[0, 13, 14] == 1.0
        assert dilated[0, 15, 14] == 1.0
        assert dilated[0, 14, 13] == 1.0
        assert dilated[0, 14, 15] == 1.0

    def test_shape_preserved(self):
        """Output shape should match input"""
        tensor = torch.zeros(1, 28, 28)
        tensor[0, 10:15, 10:15] = 1.0

        dilated = dilate_strokes(tensor)
        assert dilated.shape == (1, 28, 28)

    def test_empty_tensor(self):
        """Empty tensor stays empty"""
        tensor = torch.zeros(1, 28, 28)
        dilated = dilate_strokes(tensor)
        assert dilated.sum() == 0


# === Center of Mass Tests ===


class TestCenterOfMass:
    """Test center of mass calculation"""

    def test_single_pixel(self):
        """Single pixel at known location"""
        tensor = torch.zeros(1, 28, 28)
        tensor[0, 5, 10] = 1.0  # y=5, x=10

        cy, cx = center_of_mass(tensor)
        assert cy == 5.0
        assert cx == 10.0

    def test_symmetric_shape(self):
        """Symmetric shape should have center at center of shape"""
        tensor = torch.zeros(1, 28, 28)
        tensor[0, 10:15, 10:15] = 1.0  # 5x5 square at (10-14, 10-14)

        cy, cx = center_of_mass(tensor)
        assert abs(cy - 12.0) < 0.1  # Center at y=12
        assert abs(cx - 12.0) < 0.1  # Center at x=12

    def test_empty_tensor(self):
        """Empty tensor returns image center"""
        tensor = torch.zeros(1, 28, 28)
        cy, cx = center_of_mass(tensor)
        assert cy == 14.0
        assert cx == 14.0


# === Center Tensor Tests ===


class TestCenterTensor:
    """Test tensor centering"""

    def test_off_center_gets_centered(self):
        """Off-center drawing should be shifted to center"""
        tensor = torch.zeros(1, 28, 28)
        tensor[0, 5, 5] = 1.0  # Upper-left

        centered = center_tensor(tensor)

        # Original location should be empty (shifted away)
        assert centered[0, 5, 5] == 0.0
        # Should now be at center
        assert centered[0, 14, 14] == 1.0

    def test_already_centered(self):
        """Already centered drawing should not move much"""
        tensor = torch.zeros(1, 28, 28)
        tensor[0, 14, 14] = 1.0

        centered = center_tensor(tensor)

        # Should still be at center
        assert centered[0, 14, 14] == 1.0

    def test_shape_preserved(self):
        """Output shape should match input"""
        tensor = torch.zeros(1, 28, 28)
        tensor[0, 5:10, 5:10] = 1.0

        centered = center_tensor(tensor)
        assert centered.shape == (1, 28, 28)


# === Gaussian Kernel Tests ===


class TestGaussianKernel:
    """Test Gaussian kernel generation"""

    def test_kernel_shape(self):
        """Kernel should have correct shape"""
        kernel = gaussian_kernel(3, 1.0)
        assert kernel.shape == (3, 3)

    def test_kernel_normalized(self):
        """Kernel should sum to 1"""
        kernel = gaussian_kernel(5, 1.0)
        assert abs(kernel.sum().item() - 1.0) < 1e-6

    def test_kernel_center_highest(self):
        """Center of kernel should be highest value"""
        kernel = gaussian_kernel(5, 1.0)
        assert kernel[2, 2] == kernel.max()


# === Gaussian Blur Tests ===


class TestGaussianBlur:
    """Test Gaussian blur"""

    def test_smooths_edges(self):
        """Blur should create gradient at edges"""
        tensor = torch.zeros(1, 28, 28)
        tensor[0, 10:18, 10:18] = 1.0  # Sharp 8x8 square

        blurred = gaussian_blur(tensor)

        # Edge pixels should have intermediate values
        assert 0 < blurred[0, 9, 14] < 1.0  # Above square
        assert 0 < blurred[0, 18, 14] < 1.0  # Below square

    def test_shape_preserved(self):
        """Output shape should match input"""
        tensor = torch.zeros(1, 28, 28)
        tensor[0, 14, 14] = 1.0

        blurred = gaussian_blur(tensor)
        assert blurred.shape == (1, 28, 28)

    def test_empty_stays_empty(self):
        """Empty tensor should stay empty"""
        tensor = torch.zeros(1, 28, 28)
        blurred = gaussian_blur(tensor)
        assert blurred.sum() == 0


# === Enhanced canvas_to_tensor Tests ===


class TestCanvasToTensorEnhanced:
    """Integration tests for enhanced canvas_to_tensor"""

    def test_flags_default_true(self):
        """All preprocessing flags default to True"""
        points = [{"x": 100, "y": 100}]

        # With all preprocessing (default)
        result_full = canvas_to_tensor(points)

        # Without preprocessing
        result_none = canvas_to_tensor(points, dilate=False, center=False, blur=False)

        # Results should be different
        assert not torch.allclose(result_full, result_none)

    def test_disable_dilation(self):
        """Can disable dilation"""
        points = [{"x": 200, "y": 200}]
        result = canvas_to_tensor(points, dilate=False, center=False, blur=False)

        # Should have minimal pixels (just the points)
        assert result.sum() < 5

    def test_line_interpolation(self):
        """Lines should connect distant points"""
        # Two distant points
        points = [{"x": 0, "y": 200}, {"x": 400, "y": 200}]

        result = canvas_to_tensor(points, dilate=False, center=False, blur=False)

        # Should have filled line from left to right at y=13
        y_idx = int(200 * 27 / 400)
        assert result[0, y_idx, :].sum() > 20  # Many pixels filled

    def test_output_normalized(self):
        """Output should be in 0-1 range"""
        points = [{"x": 200, "y": 200}]
        result = canvas_to_tensor(points)

        assert result.min() >= 0.0
        assert result.max() <= 1.0

    def test_output_shape(self):
        """Output shape should be (1, 28, 28)"""
        points = [{"x": 200, "y": 200}]
        result = canvas_to_tensor(points)
        assert result.shape == (1, 28, 28)
