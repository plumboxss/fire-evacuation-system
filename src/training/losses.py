"""
Loss functions for fire prediction model training.

Implements Week 9–11 training. See docs/manual_v2.md.

Provides MSE, MAE, and channel-weighted losses operating on
normalised tensors of shape (B, C, 60, 40, 6).
"""
from __future__ import annotations

from typing import Optional


def mse_loss(pred, target, mask: Optional[object] = None):
    """Mean squared error over all elements (or fluid cells only).

    Args:
        pred: ``(B, C, 60, 40, 6)``, normalised [0, 1].
        target: ``(B, C, 60, 40, 6)``, normalised [0, 1].
        mask: Optional fluid mask ``(60, 40, 6)`` or ``(B, 1, 60, 40, 6)``.
              If provided, loss is computed only over fluid cells (mask=1).

    Returns:
        Scalar MSE loss tensor.
    """
    raise NotImplementedError("Week 9: implement masked MSE loss")


def mae_loss(pred, target, mask: Optional[object] = None):
    """Mean absolute error over all elements (or fluid cells only).

    Args:
        pred: ``(B, C, 60, 40, 6)``.
        target: ``(B, C, 60, 40, 6)``.
        mask: Optional fluid mask. Same convention as :func:`mse_loss`.

    Returns:
        Scalar MAE loss tensor.
    """
    raise NotImplementedError("Week 9: implement masked MAE loss")


def channel_weighted_loss(pred, target, weights: list[float]):
    """Weighted sum of per-channel MSE losses.

    Args:
        pred: ``(B, 3, 60, 40, 6)``.
        target: ``(B, 3, 60, 40, 6)``.
        weights: List of 3 floats ``[w_T, w_V, w_CO]``.
                 Need not sum to 1.

    Returns:
        Scalar weighted loss tensor.

    Raises:
        ValueError: If ``len(weights) != pred.shape[1]``.
    """
    raise NotImplementedError("Week 9: implement per-channel weighted loss")


if __name__ == "__main__":
    print("losses.py — skeleton only (not yet implemented)")
    print("SKIP")
