"""
Visualise risk maps and ASET fields.

Implements Week 14. See docs/manual_v2.md.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np


def plot_danger_map(
    danger: np.ndarray,
    z_index: int = 1,
    t_index: int = 0,
    output_path: Optional[Path] = None,
) -> None:
    """Plot a 2-D danger map slice with a red-to-safe colour scale.

    Args:
        danger: Shape ``(T, 60, 40, 6)`` or ``(60, 40, 6)``, values in [0, 1].
        z_index: Z layer index (0–5).
        t_index: Time frame index.
        output_path: Optional save path.
    """
    raise NotImplementedError("Week 14: plot aggregated danger field")


def plot_aset_map(
    aset: np.ndarray,
    z_index: int = 1,
    output_path: Optional[Path] = None,
) -> None:
    """Plot an ASET (Available Safe Egress Time) map.

    Args:
        aset: Shape ``(60, 40, 6)``, values in seconds [0, 300].
        z_index: Z layer index.
        output_path: Optional save path.
    """
    raise NotImplementedError("Week 14: plot ASET map with seconds colour scale")


if __name__ == "__main__":
    print("plot_risk.py — skeleton only (not yet implemented)")
    print("SKIP")
