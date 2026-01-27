"""MNIST training script with PyTorch."""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from pathlib import Path

from guessme.model.cnn import MNISTNet


def get_device() -> torch.device:
    """Get best available device (MPS > CUDA > CPU)."""
    if torch.backends.mps.is_available():
        return torch.device("mps")
    elif torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def get_dataloaders(batch_size: int = 64) -> tuple[DataLoader, DataLoader]:
    """Create train and test dataloaders for MNIST.

    Args:
        batch_size: Number of images per batch

    Returns:
        (train_loader, test_loader)
    """
    # MNIST normalization values
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])

    # Download and load datasets
    data_dir = Path(__file__).parent / "data"

    train_dataset = datasets.MNIST(
        root=data_dir,
        train=True,
        download=True,
        transform=transform
    )

    test_dataset = datasets.MNIST(
        root=data_dir,
        train=False,
        download=True,
        transform=transform
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False
    )

    return train_loader, test_loader


def train_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    device: torch.device
) -> float:
    """Train for one epoch.

    Args:
        model: The CNN model
        loader: Training data loader
        optimizer: Optimizer (e.g., Adam)
        criterion: Loss function (e.g., CrossEntropyLoss)
        device: Device to train on

    Returns:
        Average loss for the epoch
    """
    model.train()
    total_loss = 0.0

    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)

        # Forward pass
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)

        # Backward pass
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    return total_loss / len(loader)


def evaluate(
    model: nn.Module,
    loader: DataLoader,
    device: torch.device
) -> float:
    """Evaluate model accuracy.

    Args:
        model: The CNN model
        loader: Test data loader
        device: Device to evaluate on

    Returns:
        Accuracy (0-100%)
    """
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    return 100 * correct / total


def main(epochs: int = 5, batch_size: int = 64, lr: float = 0.001) -> None:
    """Train MNIST model and save weights.

    Args:
        epochs: Number of training epochs
        batch_size: Batch size for training
        lr: Learning rate
    """
    # Setup
    device = get_device()
    print(f"Using device: {device}")

    # Data
    train_loader, test_loader = get_dataloaders(batch_size)
    print(f"Train: {len(train_loader.dataset)} images")
    print(f"Test: {len(test_loader.dataset)} images")

    # Model
    model = MNISTNet().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    # Train
    best_acc = 0.0
    for epoch in range(epochs):
        loss = train_epoch(model, train_loader, optimizer, criterion, device)
        acc = evaluate(model, test_loader, device)

        print(f"Epoch {epoch+1}/{epochs} | Loss: {loss:.4f} | Acc: {acc:.2f}%")

        # Save best model
        if acc > best_acc:
            best_acc = acc
            weights_dir = Path(__file__).parent / "weights"
            weights_dir.mkdir(exist_ok=True)
            torch.save(model.state_dict(), weights_dir / "mnist_cnn.pt")
            print(f"  → Saved best model (acc: {acc:.2f}%)")

    print(f"\nTraining complete! Best accuracy: {best_acc:.2f}%")


if __name__ == "__main__":
    main()