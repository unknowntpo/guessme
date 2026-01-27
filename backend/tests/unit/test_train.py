"""Tests for training functions."""

from guessme.model.train import get_dataloaders, get_device


def test_get_device():
    """Should return a valid device."""
    device = get_device()
    assert device.type in ("mps", "cuda", "cpu")


def test_get_dataloaders():
    """Should return train and test loaders."""
    train_loader, test_loader = get_dataloaders(batch_size=32)

    # Check sizes
    assert len(train_loader.dataset) == 60000
    assert len(test_loader.dataset) == 10000

    # Check batch shape
    images, labels = next(iter(train_loader))
    assert images.shape == (32, 1, 28, 28)
    assert labels.shape == (32,)
