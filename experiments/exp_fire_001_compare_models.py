"""
Experiment: Compare ConvLSTM vs PI-FNO fire prediction accuracy.

Implements Week 14 experiment. See docs/manual_v2.md.

Loads the best checkpoint for each model, runs evaluation on the val
and OOD splits, and produces a comparison table logged to W&B.

Usage:
    python experiments/exp_fire_001_compare_models.py \\
        --conv-lstm checkpoints/conv_lstm/best.pt \\
        --pi-fno    checkpoints/pi_fno/best.pt
"""
from __future__ import annotations

from pathlib import Path


def main(
    conv_lstm_ckpt: Path,
    pi_fno_ckpt: Path,
    dataset_path: Path = Path("data/processed/dataset.h5"),
    output_dir: Path = Path("results"),
) -> None:
    """Run the model comparison experiment.

    Args:
        conv_lstm_ckpt: Path to best ConvLSTM3D checkpoint.
        pi_fno_ckpt: Path to best PI-FNO checkpoint.
        dataset_path: Processed HDF5 dataset path.
        output_dir: Where to write results CSV and figures.
    """
    raise NotImplementedError("Week 14: run comparison experiment")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--conv-lstm", type=Path, required=True)
    parser.add_argument("--pi-fno", type=Path, required=True)
    parser.add_argument("--data", type=Path, default=Path("data/processed/dataset.h5"))
    parser.add_argument("--output", type=Path, default=Path("results"))
    args = parser.parse_args()

    main(args.conv_lstm, args.pi_fno, args.data, args.output)
