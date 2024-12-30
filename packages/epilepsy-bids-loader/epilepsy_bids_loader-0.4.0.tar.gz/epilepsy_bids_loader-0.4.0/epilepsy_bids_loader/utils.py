import torch
from torch import Tensor


class Status:

    def __init__(self, msg: str) -> None:
        self.msg = msg
        return

    def update(self, status: str):
        print(f"\r\x1b[K{self.msg} {status}", end="", flush=True)
        return

    def done(self):
        print(f"\r\x1b[K{self.msg} done!", flush=True)
        return


class ZScoreScaler:
    """
    Derived from sklearn.preprocessing.StandardScaler to handle
    3D input (N, C, L) where StandardScaler can only handle 2D (L, C) input.
    """
    def __init__(self) -> None:
        self.u: Tensor = None # mean (C,)
        self.s: Tensor = None # standard deviation (C,)

    def fit(self, x: Tensor):
        """
        x: (N, C, L)
        """
        self.u = x.mean(axis=(0, 2), keepdims=True)
        self.s = x.std(axis=(0, 2), keepdims=True)
        return

    def transform(self, x: Tensor):
        """
        x: (N, C, L)
        """
        with torch.no_grad():
            return (x - self.u) / self.s