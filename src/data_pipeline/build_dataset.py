"""
End-to-end dataset builder: FDS raw → processed HDF5.

Implements Week 5–6 data pipeline. See docs/manual_v2.md.

Orchestrates FDS extraction, mask generation, normalisation, and train/val/OOD
split assignment. Writes everything to ``data/processed/dataset.h5``.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional


def build(
    raw_dir: Path,
    output_path: Path,
    seed: int = 42,
) -> None:
    """Build the full processed dataset from raw FDS outputs.

    Reads all 30 scenario directories under ``raw_dir``, extracts slices,
    generates masks, applies normalisation, and writes a single HDF5 file.

    Args:
        raw_dir: Path to ``data/raw/`` containing 30 scenario directories.
        output_path: Destination path for the HDF5 file (e.g.
                     ``data/processed/dataset.h5``). Parent directory must
                     exist.
        seed: Random seed for train/val/OOD split assignment.

    Raises:
        FileNotFoundError: If ``raw_dir`` does not exist or contains fewer
                           than 30 scenario directories.
        ValueError: If any scenario produces unexpected tensor shapes.

    Notes:
        HDF5 layout (see data/README.md for full spec):
            /scenario_{i:03d}/input   (31, 5, 60, 40, 6)
            /scenario_{i:03d}/target  (31, 3, 60, 40, 6)
            /metadata/train_indices   (24,)
            /metadata/val_indices     (3,)
            /metadata/ood_indices     (3,)
    """
    raise NotImplementedError("Week 6: orchestrate full data pipeline")


if __name__ == "__main__":
    print("build_dataset.py — skeleton only (not yet implemented)")
    print("SKIP")
