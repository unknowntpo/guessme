import torch

from guessme.model.cnn import MNISTNet


def test_cnn_forward_shape():
    """
    Input:(batch,1, 28, 28) -> Output: (batch,10)
    """
    model = MNISTNet()
    x = torch.randn(1, 1, 28, 28)
    out = model(x)
    assert out.shape == (1, 10)
