"""
Single-model evaluation runner.

Implements Week 14 evaluation. See docs/manual_v2.md.

Loads a trained checkpoint, runs inference over a dataset split,
and produces a metrics report saved to results/.
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal


def evaluate(
    checkpoint_path: Path,
    dataset_path: Path,
    split: Literal["val", "ood"] = "val",
    output_dir: Path = Path("results"),
) -> dict:
    """Evaluate a trained model on the specified split.

    Args:
        checkpoint_path: Path to a ``.pt`` model checkpoint.
        dataset_path: Path to ``data/processed/dataset.h5``.
        split: Dataset split to evaluate on: ``"val"`` or ``"ood"``.
        output_dir: Directory for results JSON and figures.

    Returns:
        Dict of metric name → value (same format as
        :func:`src.evaluation.metrics.summarise_metrics`).

    Raises:
        FileNotFoundError: If checkpoint or dataset not found.
    """
    raise NotImplementedError("Week 14: implement evaluation loop")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate a trained model checkpoint")
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--data", type=Path, default=Path("data/processed/dataset.h5"))
    parser.add_argument("--split", choices=["val", "ood"], default="val")
    parser.add_argument("--output", type=Path, default=Path("results"))
    args = parser.parse_args()

    results = evaluate(args.checkpoint, args.data, args.split, args.output)
    for k, v in results.items():
        print(f"  {k}: {v:.4f}")
