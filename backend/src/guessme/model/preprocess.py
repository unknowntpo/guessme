"""MNIST preprocessing module.

Converts canvas drawings to MNIST-compatible tensors with preprocessing
stages that improve recognition accuracy by matching MNIST training data
characteristics.

Problem: User drawings from canvas have gaps between mouse positions and
may be off-center, resulting in poor model predictions (e.g., "7" predicted
as "5" with 50% confidence).

Solution: Apply preprocessing to bridge the gap between raw canvas input
and MNIST training data characteristics:

1. Line Interpolation (Bresenham): Canvas sends discrete mouse positions
   with gaps. Bresenham's algorithm fills pixels between consecutive points
   to create continuous strokes.

2. Stroke Dilation (optional, disabled by default): Thickens 1px strokes
   using max_pool2d. Disabled by default as it can fill small holes in
   digits like "8" or "0".

3. Center of Mass Centering: MNIST digits are centered in the 28x28 frame.
   This shifts user drawings to match, using torch.roll for efficient
   circular shifting.

4. Gaussian Blur: Applies anti-aliasing to smooth jagged edges from
   pixelation, matching MNIST's smoother stroke appearance.
"""

import torch
import torch.nn.functional as F

CANVAS_SIZE = 400  # Frontend canvas is 400x400 pixels


# === Line Interpolation (Bresenham) ===


def bresenham_line(x0: int, y0: int, x1: int, y1: int) -> list[tuple[int, int]]:
    """Generate all points on a line using Bresenham's algorithm.

    Uses integer-only arithmetic for efficient pixel-perfect line drawing.
    Connects two points with no gaps.

    Args:
        x0, y0: Start point coordinates
        x1, y1: End point coordinates

    Returns:
        List of (x, y) tuples for all pixels on the line
    """
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    x, y = x0, y0
    while True:
        points.append((x, y))
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
    return points


def draw_lines_on_tensor(
    img: torch.Tensor, scaled_points: list[tuple[int, int]]
) -> None:
    """Draw connected lines between consecutive points on tensor.

    Modifies tensor in-place. Uses Bresenham's algorithm to fill gaps
    between discrete mouse positions from canvas.

    Args:
        img: 2D tensor (28x28) to draw on, modified in-place
        scaled_points: List of (x, y) tuples in tensor coordinates (0-27)
    """
    if len(scaled_points) < 2:
        return

    for i in range(len(scaled_points) - 1):
        x0, y0 = scaled_points[i]
        x1, y1 = scaled_points[i + 1]
        line_points = bresenham_line(x0, y0, x1, y1)
        for x, y in line_points:
            if 0 <= x <= 27 and 0 <= y <= 27:
                img[y, x] = 1.0


# === Stroke Dilation ===


def dilate_strokes(tensor: torch.Tensor, kernel_size: int = 3) -> torch.Tensor:
    """Dilate strokes using max pooling with same padding.

    Thickens 1px strokes to ~2-3px to match MNIST training data
    which has thick filled strokes.

    Args:
        tensor: Input tensor of shape (1, 28, 28)
        kernel_size: Size of dilation kernel (default 3)

    Returns:
        Dilated tensor of same shape
    """
    # Add batch dim for max_pool2d: (1, 28, 28) -> (1, 1, 28, 28)
    x = tensor.unsqueeze(0)
    padding = kernel_size // 2
    dilated = F.max_pool2d(x, kernel_size, stride=1, padding=padding)
    return dilated.squeeze(0)


# === Center of Mass Centering ===


def center_of_mass(tensor: torch.Tensor) -> tuple[float, float]:
    """Calculate center of mass of non-zero pixels.

    Args:
        tensor: Input tensor of shape (1, 28, 28) or (28, 28)

    Returns:
        (cy, cx) center of mass coordinates, or (14, 14) if empty
    """
    img = tensor.squeeze()  # Ensure 2D

    total_mass = img.sum()
    if total_mass == 0:
        return (14.0, 14.0)  # Return center if empty

    # Create coordinate grids
    y_coords = torch.arange(28, dtype=torch.float32, device=tensor.device)
    x_coords = torch.arange(28, dtype=torch.float32, device=tensor.device)

    # Weighted average of coordinates
    cy = (img.sum(dim=1) * y_coords).sum() / total_mass
    cx = (img.sum(dim=0) * x_coords).sum() / total_mass

    return (cy.item(), cx.item())


def center_tensor(tensor: torch.Tensor) -> torch.Tensor:
    """Shift tensor so center of mass is at image center.

    MNIST digits are centered; this aligns user drawings with training data.
    Uses torch.roll for efficient circular shifting.

    Args:
        tensor: Input tensor of shape (1, 28, 28)

    Returns:
        Centered tensor of same shape
    """
    cy, cx = center_of_mass(tensor)
    target_y, target_x = 14.0, 14.0

    # Calculate shift amounts
    shift_y = round(target_y - cy)
    shift_x = round(target_x - cx)

    # Roll shifts circularly, which works well for centering
    # First shift along y-axis (dim=1), then x-axis (dim=2)
    shifted = torch.roll(tensor, shifts=shift_y, dims=1)
    shifted = torch.roll(shifted, shifts=shift_x, dims=2)

    return shifted


# === Gaussian Blur ===


def gaussian_kernel(size: int = 3, sigma: float = 1.0) -> torch.Tensor:
    """Create 2D Gaussian kernel for convolution.

    Args:
        size: Kernel size (must be odd)
        sigma: Standard deviation of Gaussian

    Returns:
        2D tensor of shape (size, size), normalized to sum to 1
    """
    coords = torch.arange(size, dtype=torch.float32) - size // 2
    g = torch.exp(-(coords**2) / (2 * sigma**2))
    kernel = g.outer(g)
    return kernel / kernel.sum()


def gaussian_blur(
    tensor: torch.Tensor, kernel_size: int = 3, sigma: float = 1.0
) -> torch.Tensor:
    """Apply Gaussian blur for anti-aliasing.

    Smooths strokes to reduce jagged edges, matching MNIST's
    anti-aliased appearance.

    Args:
        tensor: Input tensor of shape (1, 28, 28)
        kernel_size: Size of Gaussian kernel (must be odd)
        sigma: Standard deviation of Gaussian

    Returns:
        Blurred tensor of same shape
    """
    kernel = gaussian_kernel(kernel_size, sigma)
    # Reshape kernel for conv2d: (out_channels, in_channels, H, W)
    kernel = kernel.view(1, 1, kernel_size, kernel_size).to(tensor.device)

    # Add batch dim: (1, 28, 28) -> (1, 1, 28, 28)
    x = tensor.unsqueeze(0)
    padding = kernel_size // 2
    blurred = F.conv2d(x, kernel, padding=padding)
    return blurred.squeeze(0)


# === ASCII Visualization ===


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
def canvas_to_tensor(
    points: list[dict],
    debug: bool = False,
    dilate: bool = False,
    center: bool = True,
    blur: bool = True,
) -> torch.Tensor:
    """Convert canvas points to MNIST-compatible tensor.

    Bridges the gap between raw canvas input and MNIST training data:
    - Canvas: 400x400px, discrete mouse events with gaps, arbitrary position
    - MNIST: 28x28px, continuous strokes, centered digits, anti-aliased

    Preprocessing pipeline:
    1. Scale 400x400 canvas coords to 28x28 tensor coords
    2. Line interpolation (Bresenham) - fills gaps between mouse positions
    3. Dilation (optional) - thickens strokes, but can fill holes in 8/0/6/9
    4. Centering - shifts to center of mass for MNIST alignment
    5. Gaussian blur - anti-aliasing for smoother edges

    Args:
        points: List of {"x": float, "y": float} from canvas (0-400 range)
        debug: If True, print ASCII representation of the tensor
        dilate: If True, apply stroke dilation (default False - fills holes)
        center: If True, center drawing by center of mass (default True)
        blur: If True, apply Gaussian blur (default True)

    Returns:
        Tensor of shape (1, 28, 28), values normalized to 0-1 range
    """
    # Create blank 28x28 image
    img = torch.zeros(28, 28)

    # Scale canvas coords (0-400) to tensor coords (0-27)
    scaled_points = []
    for p in points:
        x = int(p["x"] * 27 / CANVAS_SIZE)
        y = int(p["y"] * 27 / CANVAS_SIZE)
        x = max(0, min(27, x))  # Clamp bounds
        y = max(0, min(27, y))
        scaled_points.append((x, y))

    # Draw individual points
    for x, y in scaled_points:
        img[y, x] = 1.0

    # Draw lines connecting consecutive points (fills gaps)
    draw_lines_on_tensor(img, scaled_points)

    result = img.unsqueeze(0)

    # Apply preprocessing stages
    if dilate:
        result = dilate_strokes(result)

    if center:
        result = center_tensor(result)

    if blur:
        result = gaussian_blur(result)

    # Clamp values to 0-1 range after processing
    result = torch.clamp(result, 0.0, 1.0)

    if debug:
        print_ascii(result)

    return result
