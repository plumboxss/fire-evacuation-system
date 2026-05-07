"""
Evaluation metrics for fire prediction models.

Implements Week 14 evaluation. See docs/manual_v2.md.

All metrics operate on normalised tensors of shape (B, 3, 60, 40, 6)
unless otherwise noted.
"""
from __future__ import annotations

import numpy as np
from typing import Dict


def rmse_per_channel(pred: np.ndarray, target: np.ndarray) -> np.ndarray:
    """Root mean squared error for each output channel.

    Args:
        pred: ``(B, 3, 60, 40, 6)``, normalised [0, 1].
        target: ``(B, 3, 60, 40, 6)``, normalised [0, 1].

    Returns:
        Array of shape ``(3,)`` — RMSE for [T, V, CO] channels.

    Raises:
        ValueError: If shapes of ``pred`` and ``target`` do not match.
    """
    raise NotImplementedError("Week 14: compute per-channel RMSE")


def mae_per_channel(pred: np.ndarray, target: np.ndarray) -> np.ndarray:
    """Mean absolute error for each output channel.

    Args:
        pred: ``(B, 3, 60, 40, 6)``.
        target: ``(B, 3, 60, 40, 6)``.

    Returns:
        Array of shape ``(3,)`` — MAE for [T, V, CO].
    """
    raise NotImplementedError("Week 14: compute per-channel MAE")


def ssim_per_channel(pred: np.ndarray, target: np.ndarray) -> np.ndarray:
    """Structural Similarity Index (SSIM) for each output channel.

    Computed as the mean SSIM over all (ny, nz) slices across the X axis
    and all batch samples.

    Args:
        pred: ``(B, 3, 60, 40, 6)``.
        target: ``(B, 3, 60, 40, 6)``.

    Returns:
        Array of shape ``(3,)`` — SSIM for [T, V, CO], values in [-1, 1].
    """
    raise NotImplementedError("Week 14: compute per-channel SSIM using skimage")


def peak_danger_error(pred: np.ndarray, target: np.ndarray) -> float:
    """Mean absolute error of the peak danger value per sample.

    Peak danger is the maximum cell value across all spatial dimensions
    for the temperature channel (channel 0).

    Args:
        pred: ``(B, 3, 60, 40, 6)``.
        target: ``(B, 3, 60, 40, 6)``.

    Returns:
        Scalar — mean |max(pred_T) − max(target_T)| over batch.
    """
    raise NotImplementedError("Week 14: compute peak danger error")


def fed_error(pred_co: np.ndarray, target_co: np.ndarray, dt: float = 10.0) -> float:
    """Mean absolute error of the accumulated FED over a trajectory.

    Integrates FED along the time axis for both prediction and target CO
    fields and returns the mean absolute difference.

    Args:
        pred_co: ``(T, 60, 40, 6)`` — predicted CO channel (normalised).
        target_co: ``(T, 60, 40, 6)`` — ground-truth CO channel (normalised).
        dt: Time step in seconds.

    Returns:
        Scalar — mean |FED_pred − FED_target| over all cells.
    """
    raise NotImplementedError("Week 14: compute FED accumulation error")


def summarise_metrics(
    pred: np.ndarray, target: np.ndarray
) -> Dict[str, float]:
    """Compute all metrics and return a flat dict for W&B logging.

    Args:
        pred: ``(B, 3, 60, 40, 6)``.
        target: ``(B, 3, 60, 40, 6)``.

    Returns:
        Dict with keys like ``"rmse/T"``, ``"rmse/V"``, ``"rmse/CO"``,
        ``"mae/T"``, etc.
    """
    raise NotImplementedError("Week 14: assemble full metrics dict")


if __name__ == "__main__":
    print("metrics.py — skeleton only (not yet implemented)")
    print("SKIP")
