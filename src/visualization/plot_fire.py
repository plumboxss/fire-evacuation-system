"""
Visualise fire field predictions (temperature, visibility, CO).

Implements Week 14. See docs/manual_v2.md.

Produces 2-D horizontal slice plots at a specified Z layer.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np


def plot_field_slice(
    field: np.ndarray,
    channel_name: str,
    z_index: int = 1,
    t_index: int = 0,
    output_path: Optional[Path] = None,
    title: Optional[str] = None,
) -> None:
    """Plot a horizontal (X–Y) slice of a fire field.

    Args:
        field: Array of shape ``(T, C, 60, 40, 6)`` or ``(C, 60, 40, 6)``
               or ``(60, 40, 6)``. Normalised [0, 1].
        channel_name: One of ``"temperature"``, ``"visibility"``, ``"co"``.
        z_index: Z layer index (0–5). Default 1 (≈ 1 m above floor).
        t_index: Time frame index. Used only if field has a time dimension.
        output_path: If provided, save figure to this path. Otherwise show.
        title: Optional plot title.

    Raises:
        ValueError: If ``z_index`` not in [0, 5].
    """
    raise NotImplementedError("Week 14: implement 2-D slice plot with matplotlib")


def plot_comparison(
    pred: np.ndarray,
    target: np.ndarray,
    channel_name: str,
    z_index: int = 1,
    t_index: int = 0,
    output_path: Optional[Path] = None,
) -> None:
    """Plot prediction vs ground truth side by side.

    Args:
        pred: ``(3, 60, 40, 6)`` predicted field.
        target: ``(3, 60, 40, 6)`` ground-truth field.
        channel_name: Channel to display.
        z_index: Z layer index.
        t_index: Time frame index.
        output_path: Optional save path.
    """
    raise NotImplementedError("Week 14: implement side-by-side comparison plot")


if __name__ == "__main__":
    print("plot_fire.py — skeleton only (not yet implemented)")
    print("SKIP")
