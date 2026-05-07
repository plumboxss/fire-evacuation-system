"""
Available Safe Egress Time (ASET) computation.

Implements Week 12. See docs/manual_v2.md.

ASET is the time at which each cell becomes untenable (danger ≥ threshold).
It is used to colour-code the evacuation urgency map.
"""
from __future__ import annotations

import numpy as np


def compute_aset(
    danger_sequence: np.ndarray,
    times: np.ndarray,
    threshold: float = 0.5,
) -> np.ndarray:
    """Compute Available Safe Egress Time for each grid cell.

    Finds the first frame at which the danger value crosses ``threshold``.

    Args:
        danger_sequence: Danger field over time, shape ``(T, 60, 40, 6)``,
                         values in [0, 1]. Higher = more dangerous.
        times: 1-D array of frame times in seconds, length ``T``.
        threshold: Danger level at which a cell becomes untenable.
                   Default 0.5.

    Returns:
        ASET array of shape ``(60, 40, 6)`` in seconds.
        Cells that never reach the threshold are assigned ``times[-1]``
        (i.e., ASET = T_END = 300 s).

    Raises:
        ValueError: If ``danger_sequence.shape[0] != len(times)``.
    """
    raise NotImplementedError("Week 12: find first crossing of danger threshold per cell")


if __name__ == "__main__":
    print("aset.py — skeleton only (not yet implemented)")
    print("SKIP")
