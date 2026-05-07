"""
Dataset integrity verification.

Implements Week 5–6 data pipeline. See docs/manual_v2.md.

Checks the processed HDF5 dataset for shape consistency, value ranges,
and correct split assignment.
"""
from __future__ import annotations

from pathlib import Path


def verify_dataset(dataset_path: Path, verbose: bool = True) -> bool:
    """Verify a processed HDF5 dataset for shape, range, and split integrity.

    Args:
        dataset_path: Path to ``data/processed/dataset.h5``.
        verbose: If True, print per-check results to stdout.

    Returns:
        True if all checks pass, False otherwise.

    Raises:
        FileNotFoundError: If ``dataset_path`` does not exist.

    Checks performed:
        - All 30 scenarios present.
        - Input shape: (31, 5, 60, 40, 6).
        - Target shape: (31, 3, 60, 40, 6).
        - All values in [0, 1].
        - Train/val/OOD indices present and non-overlapping.
        - Split counts: 24 / 3 / 3.
    """
    raise NotImplementedError("Week 6: implement dataset integrity checks")


if __name__ == "__main__":
    print("verify.py — skeleton only (not yet implemented)")
    print("SKIP")
