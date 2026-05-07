"""
Visualise evacuation paths overlaid on the building floor plan.

Implements Week 14. See docs/manual_v2.md.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import numpy as np


def plot_evacuation_path(
    waypoints: List[np.ndarray],
    danger: Optional[np.ndarray] = None,
    z_index: int = 1,
    exits: Optional[List] = None,
    output_path: Optional[Path] = None,
) -> None:
    """Plot an evacuation path on the building floor plan.

    Args:
        waypoints: Ordered list of world-space coordinates ``[x, y, z]`` in metres.
        danger: Optional ``(60, 40, 6)`` background danger field.
        z_index: Z layer for background slice.
        exits: Optional list of exit coordinates to mark on the plot.
        output_path: If provided, save figure to this path.
    """
    raise NotImplementedError("Week 14: overlay path on building map")


def plot_replanning_sequence(
    paths: List[List[np.ndarray]],
    times: List[float],
    output_path: Optional[Path] = None,
) -> None:
    """Plot a sequence of re-planned paths (one per re-planning step).

    Args:
        paths: List of path waypoint lists, one per re-plan event.
        times: Times in seconds at which each path was computed.
        output_path: Optional save path.
    """
    raise NotImplementedError("Week 14: plot dynamic re-planning sequence")


if __name__ == "__main__":
    print("plot_paths.py — skeleton only (not yet implemented)")
    print("SKIP")
