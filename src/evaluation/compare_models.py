"""
Side-by-side comparison of ConvLSTM and PI-FNO checkpoints.

Implements Week 14 evaluation. See docs/manual_v2.md.

Produces a comparison table and figures saved to results/ and figures/.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict


def compare(
    conv_lstm_ckpt: Path,
    pi_fno_ckpt: Path,
    dataset_path: Path,
    output_dir: Path = Path("results"),
) -> Dict[str, Dict[str, float]]:
    """Compare ConvLSTM and PI-FNO on the val and OOD splits.

    Args:
        conv_lstm_ckpt: Path to ConvLSTM3D checkpoint.
        pi_fno_ckpt: Path to PI-FNO checkpoint.
        dataset_path: Path to ``data/processed/dataset.h5``.
        output_dir: Directory for comparison results.

    Returns:
        Nested dict: ``{model_name: {metric_name: value}}``.

    Raises:
        FileNotFoundError: If either checkpoint is missing.
    """
    raise NotImplementedError("Week 14: run both models and aggregate comparison metrics")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Compare ConvLSTM vs PI-FNO")
    parser.add_argument("--conv-lstm", type=Path, required=True)
    parser.add_argument("--pi-fno", type=Path, required=True)
    parser.add_argument("--data", type=Path, default=Path("data/processed/dataset.h5"))
    parser.add_argument("--output", type=Path, default=Path("results"))
    args = parser.parse_args()

    results = compare(args.conv_lstm, args.pi_fno, args.data, args.output)
    for model, metrics in results.items():
        print(f"\n{model}:")
        for k, v in metrics.items():
            print(f"  {k}: {v:.4f}")
