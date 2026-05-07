"""
Generate fluid/solid masks from FDS geometry.

Implements Week 5–6 data pipeline. See docs/manual_v2.md.

The mask array marks cells that are physically accessible to smoke and
occupants. Solid cells (walls, floors, furniture) have mask=0.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np


def generate_mask_from_fds(fds_dir: Path) -> np.ndarray:
    """Read FDS geometry and produce a binary fluid/solid mask.

    Args:
        fds_dir: Path to the FDS scenario directory.

    Returns:
        Boolean array of shape ``(60, 40, 6)``.
        True (1) = fluid cell accessible to smoke and occupants.
        False (0) = solid cell (wall, obstacle, floor/ceiling slab).

    Raises:
        FileNotFoundError: If the FDS directory does not exist.
        ValueError: If extracted geometry does not match ``(60, 40, 6)``.
    """
    raise NotImplementedError("Week 6: extract solid/fluid mask from FDS geometry")


def default_open_floor_mask() -> np.ndarray:
    """Return a mask for an empty open-plan floor (no interior obstacles).

    The floor slab (iz=0 bottom face) and ceiling (iz=5 top face) are
    considered solid in the HVAC sense, but all 60×40×6 cells are
    returned as fluid=1 for simplicity in this project.

    Returns:
        All-ones boolean array of shape ``(60, 40, 6)``.
    """
    raise NotImplementedError("Week 6: create default open-plan mask")


if __name__ == "__main__":
    print("mask_generator.py — skeleton only (not yet implemented)")
    print("SKIP")
