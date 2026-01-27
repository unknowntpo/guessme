"""MNIST CNN model module."""

import torch


def print_ascii(tensor: torch.Tensor) -> None:
    img = tensor.squeeze()  # Remove channel dim if present
    chars = " .:-=+*#%@"  # Dark to light

    for row in img:
        line = ""
        for val in row:
            idx = int(val.item() * (len(chars) - 1))
            line += chars[idx]
        print(line)
    print()


# TODO: define points with custom struct
def canvas_to_tensor(points: list[dict]) -> torch.Tensor:
    """Convert canvas points to MNIST-compatible tensor.

    Args:
    points: List of {"x": float, "y": float} from canvas

    Returns:
    Tensor of shape (1, 28, 28), normalized 0-1
    """

    # Create blank 28x28 image
    img = torch.zeros(28, 28)

    # Draw points (scale canvas coords to 28x28)
    # FIXME: understand why it
    for p in points:
        x = int(p["x"]) % 28
        y = int(p["y"]) % 28
        img[y, x] = 1.0

    return img.unsqueeze(0)
