"""
Ablation: Effect of ConvLSTM hidden dimension on accuracy and speed.

Implements Week 10 ablation. See docs/manual_v2.md.

Trains ConvLSTM3D with hidden_dim ∈ {16, 32, 64, 128} and reports
val RMSE, parameter count, and inference latency.

Usage:
    python experiments/ablation_model_size.py
"""
from __future__ import annotations

from pathlib import Path


def main(
    dataset_path: Path = Path("data/processed/dataset.h5"),
    output_dir: Path = Path("results/ablation_model_size"),
) -> None:
    """Train ConvLSTM with varying hidden dimensions.

    Args:
        dataset_path: Processed HDF5 dataset.
        output_dir: Output directory.
    """
    raise NotImplementedError("Week 10: run model size ablation (16/32/64/128 hidden)")


if __name__ == "__main__":
    main()
