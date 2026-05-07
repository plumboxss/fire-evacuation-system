"""
Building geometry representation.

Implements Week 3–4 shared geometry. See docs/manual_v2.md.

Provides a typed BuildingGeometry object loaded from configs/building.yaml
that exposes the obstacle mask and exit locations used by the path planner.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import numpy as np
import yaml

from src.shared.constants import CELL_SIZE_M, DOMAIN_SIZE_M, GRID_SHAPE


@dataclass
class ExitLocation:
    """A named building exit in world coordinates (metres)."""

    name: str
    x: float
    y: float
    z: float


@dataclass
class BuildingGeometry:
    """Full description of the single-floor building.

    Attributes:
        domain_size_m: (Lx, Ly, Lz) in metres — always (30, 20, 3).
        grid_shape:    (nx, ny, nz) — always (60, 40, 6).
        cell_size_m:   Always 0.5 m.
        exits:         List of named exit locations.
        obstacle_mask: Boolean array (nx, ny, nz); True = solid cell.
    """

    domain_size_m: tuple[float, float, float] = DOMAIN_SIZE_M
    grid_shape: tuple[int, int, int] = GRID_SHAPE
    cell_size_m: float = CELL_SIZE_M
    exits: List[ExitLocation] = field(default_factory=list)
    obstacle_mask: np.ndarray = field(
        default_factory=lambda: np.zeros(GRID_SHAPE, dtype=bool)
    )


def load_building(config_path: Path) -> BuildingGeometry:
    """Load building geometry from a YAML configuration file.

    Args:
        config_path: Path to ``configs/building.yaml``.

    Returns:
        :class:`BuildingGeometry` populated from the config.

    Raises:
        ValueError: If config dimensions differ from project constants.
        FileNotFoundError: If ``config_path`` does not exist.
    """
    raise NotImplementedError("Week 3: load and validate building config")


def build_obstacle_mask(geometry: BuildingGeometry) -> np.ndarray:
    """Rasterise obstacle definitions into a boolean grid mask.

    Args:
        geometry: :class:`BuildingGeometry` with ``obstacles`` list populated.

    Returns:
        Boolean array of shape ``GRID_SHAPE`` (60, 40, 6).
        True indicates a solid (non-fluid) cell.
    """
    raise NotImplementedError("Week 3: rasterise obstacle boxes onto grid")


if __name__ == "__main__":
    print("building.py — skeleton only (not yet implemented)")
    print("SKIP")
