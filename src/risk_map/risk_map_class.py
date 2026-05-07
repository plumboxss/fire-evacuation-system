"""
Abstract RiskMap base class and StaticRiskMap implementation.

Implements Week 12. See docs/manual_v2.md and docs/interface_contracts.md.

The RiskMap contract is the boundary between the fire prediction pipeline
and the path planning module. See docs/interface_contracts.md §2.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

import numpy as np


class RiskMap(ABC):
    """Abstract base class for all danger-field representations.

    Any concrete implementation must honour the contract in
    docs/interface_contracts.md §2:
        - query(xyz, t) returns a scalar in [0, 1].
        - Out-of-bounds coordinates return 1.0 (maximum danger).
    """

    @abstractmethod
    def query(self, xyz: np.ndarray, t: float | None = None) -> float:
        """Return danger level at world coordinate xyz = (x, y, z) in metres.

        Args:
            xyz: 1-D numpy array of length 3: ``[x_m, y_m, z_m]``.
            t: Query time in seconds. If None, uses the latest available frame.

        Returns:
            Danger level ∈ [0, 1].
            **Always returns 1.0 for out-of-bounds coordinates.**

        Raises:
            ValueError: If ``xyz`` does not have exactly 3 elements.
        """
        raise NotImplementedError


class StaticRiskMap(RiskMap):
    """Risk map backed by a pre-computed (T, 60, 40, 6) danger array.

    Args:
        danger_array: Array of shape ``(n_frames, 60, 40, 6)``,
                      values in [0, 1]. Interpolated linearly in time.
        times: 1-D array of frame times in seconds, length ``n_frames``.
               Must be sorted ascending.

    Raises:
        ValueError: If ``danger_array.shape[1:]`` != ``(60, 40, 6)``.
    """

    def __init__(self, danger_array: np.ndarray, times: np.ndarray) -> None:
        raise NotImplementedError("Week 12: implement StaticRiskMap.__init__")

    def query(self, xyz: np.ndarray, t: float | None = None) -> float:
        """Interpolate danger from pre-computed array.

        Args:
            xyz: ``[x_m, y_m, z_m]`` in metres.
            t: Query time in seconds.

        Returns:
            Danger ∈ [0, 1]. Returns 1.0 for out-of-bounds.
        """
        raise NotImplementedError("Week 12: implement StaticRiskMap.query")

    @classmethod
    def from_npy(cls, path: Path) -> "StaticRiskMap":
        """Load a StaticRiskMap from a saved .npy or .npz file.

        Args:
            path: Path to ``.npz`` containing ``danger`` and ``times`` arrays.

        Returns:
            :class:`StaticRiskMap` instance.
        """
        raise NotImplementedError("Week 12: load StaticRiskMap from .npz")


if __name__ == "__main__":
    print("risk_map_class.py — skeleton only (not yet implemented)")
    print("SKIP")
