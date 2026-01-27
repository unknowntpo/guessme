import torch
import torch.nn as nn


class MNISTNet(nn.Module):
    # Conv layers
    def __init__(self):
        super().__init__()

        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)

        # FC layers (28 -> 14 -> 7, so 64*7*7)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

        self.relu = nn.ReLU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Conv block 1: (1, 28, 28) -> (32, 14, 14)
        x = self.pool(self.relu(self.conv1(x)))
        # Conv block 2: (32, 14, 14) -> (64, 7, 7)
        x = self.pool(self.relu(self.conv2(x)))
        # Flatten: (64, 7, 7) -> (64*7*7)
        x = x.view(x.size(0), -1)
        # FC layers
        x = self.relu(self.fc1(x))
        x = self.fc2(x)  # raw logits, no softmax
        return x
