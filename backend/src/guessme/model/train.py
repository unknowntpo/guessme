"""MNIST training script with PyTorch and MLflow tracking."""

import platform
import time
from pathlib import Path

import mlflow
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from guessme.model.cnn import MNISTNet


def get_system_info() -> dict:
    """Collect system information for MLflow logging."""
    return {
        "python_version": platform.python_version(),
        "torch_version": torch.__version__,
        "platform": platform.system(),
        "platform_release": platform.release(),
        "processor": platform.processor() or "unknown",
        "cuda_available": torch.cuda.is_available(),
        "mps_available": torch.backends.mps.is_available(),
    }


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
    transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
    )

    # Download and load datasets
    data_dir = Path(__file__).parent / "data"

    train_dataset = datasets.MNIST(
        root=data_dir, train=True, download=True, transform=transform
    )

    test_dataset = datasets.MNIST(
        root=data_dir, train=False, download=True, transform=transform
    )

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, test_loader


def train_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    device: torch.device,
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


def evaluate(model: nn.Module, loader: DataLoader, device: torch.device) -> float:
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
    # Setup MLflow
    # MLflow db in backend/ directory (4 levels up from train.py)
    backend_dir = Path(__file__).resolve().parent.parent.parent.parent
    mlflow_db = backend_dir / "mlflow.db"
    print(f"[DEBUG] MLflow DB: {mlflow_db}")
    mlflow.set_tracking_uri(f"sqlite:///{mlflow_db}")
    mlflow.set_experiment("mnist-training")

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

    with mlflow.start_run():
        # Log system info
        sys_info = get_system_info()
        mlflow.log_params({f"sys_{k}": v for k, v in sys_info.items()})

        # Log hyperparameters
        mlflow.log_params({
            "epochs": epochs,
            "batch_size": batch_size,
            "learning_rate": lr,
            "optimizer": "Adam",
            "loss_function": "CrossEntropyLoss",
            "device": str(device),
        })

        # Log dataset info
        mlflow.log_params({
            "train_samples": len(train_loader.dataset),
            "test_samples": len(test_loader.dataset),
            "num_classes": 10,
            "input_shape": "1x28x28",
        })

        # Log model architecture
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        mlflow.log_params({
            "model_name": "MNISTNet",
            "total_params": total_params,
            "trainable_params": trainable_params,
        })

        # Train
        best_acc = 0.0
        weights_dir = Path(__file__).parent / "weights"
        weights_dir.mkdir(exist_ok=True)
        start_time = time.time()

        for epoch in range(epochs):
            epoch_start = time.time()
            loss = train_epoch(model, train_loader, optimizer, criterion, device)
            acc = evaluate(model, test_loader, device)
            epoch_time = time.time() - epoch_start

            # Log metrics per epoch
            mlflow.log_metrics({
                "loss": loss,
                "accuracy": acc,
                "epoch_time_sec": epoch_time,
            }, step=epoch)
            print(f"Epoch {epoch + 1}/{epochs} | Loss: {loss:.4f} | Acc: {acc:.2f}% | Time: {epoch_time:.1f}s")

            # Save best model
            if acc > best_acc:
                best_acc = acc
                torch.save(model.state_dict(), weights_dir / "mnist_cnn.pt")
                print(f"  → Saved best model (acc: {acc:.2f}%)")

        # Log final metrics and model artifact
        total_time = time.time() - start_time
        mlflow.log_metrics({
            "best_accuracy": best_acc,
            "total_training_time_sec": total_time,
        })
        mlflow.log_artifact(str(weights_dir / "mnist_cnn.pt"))
        print(f"\nTraining complete! Best accuracy: {best_acc:.2f}% | Total time: {total_time:.1f}s")
        print(f"MLflow run ID: {mlflow.active_run().info.run_id}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train MNIST model")
    parser.add_argument("--epochs", type=int, default=5, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=64, help="Batch size")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate")
    args = parser.parse_args()

    main(epochs=args.epochs, batch_size=args.batch_size, lr=args.lr)
