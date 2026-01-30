"""MNIST CNN model module."""

import torch

CANVAS_SIZE = 400  # Frontend canvas is 400x400 pixels


def tensor_to_ascii(tensor: torch.Tensor) -> str:
    """Convert tensor to ASCII art string for visualization."""
    img = tensor.squeeze()  # Remove channel dim if present
    chars = " .:-=+*#%@"  # Dark to light

    lines = []
    for row in img:
        line = ""
        for val in row:
            idx = int(val.item() * (len(chars) - 1))
            line += chars[idx]
        lines.append(line)
    return "\n".join(lines)


def print_ascii(tensor: torch.Tensor) -> None:
    """Print ASCII art of tensor to stdout."""
    print(tensor_to_ascii(tensor))
    print()


# TODO: define points with custom struct
def canvas_to_tensor(points: list[dict], debug: bool = False) -> torch.Tensor:
    """Convert canvas points to MNIST-compatible tensor.

    Args:
    points: List of {"x": float, "y": float} from canvas
    debug: If True, print ASCII representation of the tensor

    Returns:
    Tensor of shape (1, 28, 28), normalized 0-1
    """

    # Create blank 28x28 image
    img = torch.zeros(28, 28)

    # Draw points (scale canvas coords 0-400 to 0-27)
    for p in points:
        x = int(p["x"] * 27 / CANVAS_SIZE)
        y = int(p["y"] * 27 / CANVAS_SIZE)
        x = max(0, min(27, x))  # Clamp bounds
        y = max(0, min(27, y))
        img[y, x] = 1.0

    result = img.unsqueeze(0)

    if debug:
        print_ascii(result)

    return result
