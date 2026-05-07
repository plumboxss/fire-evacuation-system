"""
Animated visualisations of fire spread and evacuation.

Implements Week 14. See docs/manual_v2.md.

Produces MP4 or GIF animations saved to figures/.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import numpy as np


def animate_fire_spread(
    field_sequence: np.ndarray,
    channel_name: str,
    z_index: int = 1,
    fps: int = 5,
    output_path: Path = Path("figures/fire_spread.mp4"),
) -> None:
    """Animate fire spread over time as a 2-D slice.

    Args:
        field_sequence: ``(T, 60, 40, 6)`` single-channel field, normalised.
        channel_name: ``"temperature"``, ``"visibility"``, or ``"co"``.
        z_index: Z layer to visualise.
        fps: Frames per second.
        output_path: Output video path.

    Raises:
        ValueError: If ``field_sequence.ndim != 4``.
    """
    raise NotImplementedError("Week 14: create animated fire spread video")


def animate_evacuation(
    danger_sequence: np.ndarray,
    trajectory: List[np.ndarray],
    times: List[float],
    z_index: int = 1,
    fps: int = 5,
    output_path: Path = Path("figures/evacuation.mp4"),
) -> None:
    """Animate an occupant following the evacuation path over the danger field.

    Args:
        danger_sequence: ``(T, 60, 40, 6)`` danger field sequence.
        trajectory: Ordered list of ``[x, y, z]`` world coordinates.
        times: Time in seconds for each trajectory point.
        z_index: Z layer for background.
        fps: Frames per second.
        output_path: Output video path.
    """
    raise NotImplementedError("Week 14: create animated evacuation video")


if __name__ == "__main__":
    print("animations.py — skeleton only (not yet implemented)")
    print("SKIP")
