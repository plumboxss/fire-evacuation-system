"""
Ablation: Effect of training data size on model accuracy.

Implements Week 14 ablation. See docs/manual_v2.md.

Trains ConvLSTM3D with 6, 12, 18, and 24 scenarios and reports val RMSE
to understand data efficiency.

Usage:
    python experiments/ablation_data_size.py
"""
from __future__ import annotations

from pathlib import Path


def main(
    dataset_path: Path = Path("data/processed/dataset.h5"),
    output_dir: Path = Path("results/ablation_data_size"),
) -> None:
    """Train ConvLSTM with varying dataset sizes.

    Args:
        dataset_path: Processed HDF5 dataset.
        output_dir: Output directory.
    """
    raise NotImplementedError("Week 14: run data size ablation (6, 12, 18, 24 scenarios)")


if __name__ == "__main__":
    main()
