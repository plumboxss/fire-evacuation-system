"""
FDS slice file extraction using fdsreader.

Implements Week 5–6 data pipeline. See docs/manual_v2.md.

Reads raw FDS *.smv / slice files for a single scenario and returns
numpy arrays of shape (31, 60, 40, 6) for each field variable.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np


def extract_slices(fds_dir: Path) -> Dict[str, np.ndarray]:
    """Extract temperature, visibility, and CO slices from an FDS scenario.

    Args:
        fds_dir: Directory containing the *.smv file and associated slices.
                 Must be a valid FDS output directory for a 30×20×3 m building.

    Returns:
        Dictionary with keys ``"temperature"``, ``"visibility"``, ``"co_ppm"``.
        Each value has shape ``(31, 60, 40, 6)`` — (time, nx, ny, nz).
        Units: temperature in °C, visibility in metres, CO in ppm.

    Raises:
        FileNotFoundError: If ``fds_dir`` does not contain an *.smv file.
        ValueError: If extracted grid shape != (60, 40, 6).
    """
    raise NotImplementedError("Week 6: implement using fdsreader library")


def list_scenarios(raw_dir: Path) -> list[Path]:
    """Return sorted list of scenario directories under ``raw_dir``.

    Args:
        raw_dir: Path to ``data/raw/``.

    Returns:
        List of :class:`pathlib.Path` objects, one per scenario directory,
        sorted alphabetically.

    Raises:
        FileNotFoundError: If ``raw_dir`` does not exist.
    """
    raise NotImplementedError("Week 6: list scenario directories")


if __name__ == "__main__":
    print("fds_extractor.py — skeleton only (not yet implemented)")
    print("SKIP")
