from guessme.model.preprocess import canvas_to_tensor


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
