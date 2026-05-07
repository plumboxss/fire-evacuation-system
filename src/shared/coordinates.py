"""
Coordinate system utilities for the fire evacuation prediction system.

Implements Week 3–4 shared geometry. See docs/manual_v2.md and
docs/coordinate_convention.md.

Coordinate conventions
----------------------
- World space : metres, Z-up, origin at building corner (0, 0, 0).
- Grid space  : integer cell indices (ix, iy, iz), 0-based.
- Cell centres: world_x = (ix + 0.5) * CELL_SIZE_M, etc.

See docs/coordinate_convention.md for the full specification.
"""
from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np

from src.shared.constants import CELL_SIZE_M, DOMAIN_SIZE_M, GRID_SHAPE


def world_to_grid(xyz: np.ndarray) -> np.ndarray:
    """Convert world coordinates (metres) to grid cell indices.

    Args:
        xyz: Array of shape (..., 3) containing (x, y, z) in metres.

    Returns:
        Integer cell indices of shape (..., 3) as (ix, iy, iz).
        Out-of-bounds coordinates produce indices outside [0, GRID_SHAPE−1].

    Raises:
        ValueError: If ``xyz`` last dimension is not 3.
    """
    raise NotImplementedError("Week 3: implement world → grid conversion")


def grid_to_world(ixyz: np.ndarray) -> np.ndarray:
    """Convert grid cell indices to world-space cell-centre coordinates.

    Args:
        ixyz: Integer array of shape (..., 3) containing (ix, iy, iz).

    Returns:
        Float array of shape (..., 3) with cell-centre (x, y, z) in metres.

    Raises:
        ValueError: If ``ixyz`` last dimension is not 3.
    """
    raise NotImplementedError("Week 3: implement grid → world conversion")


def is_in_bounds(xyz: np.ndarray) -> np.ndarray:
    """Return a boolean mask: True where world coordinates lie inside the domain.

    Args:
        xyz: Array of shape (..., 3) in metres.

    Returns:
        Boolean array of shape (...,).
    """
    raise NotImplementedError("Week 3: implement bounds check")


def cell_centres() -> np.ndarray:
    """Return the world-space centres of all grid cells.

    Returns:
        Array of shape (nx, ny, nz, 3) where the last axis is (x, y, z) in metres.
        ``GRID_SHAPE`` = (60, 40, 6).
    """
    raise NotImplementedError("Week 3: build meshgrid of all cell centres")


if __name__ == "__main__":
    print("coordinates.py — skeleton only (not yet implemented)")
    print("SKIP")
