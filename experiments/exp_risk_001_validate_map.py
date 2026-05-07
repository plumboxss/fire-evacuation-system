"""
Experiment: Validate the ISO-13571 risk map against FDS ground truth.

Implements Week 12 experiment. See docs/manual_v2.md.

Compares the danger scores produced by the risk map converter against
the ground-truth FDS fields for 3 OOD scenarios.

Usage:
    python experiments/exp_risk_001_validate_map.py \\
        --checkpoint checkpoints/pi_fno/best.pt
"""
from __future__ import annotations

from pathlib import Path


def main(
    checkpoint_path: Path,
    dataset_path: Path = Path("data/processed/dataset.h5"),
    output_dir: Path = Path("results"),
) -> None:
    """Validate risk map danger scores against FDS ground truth.

    Args:
        checkpoint_path: Trained model checkpoint.
        dataset_path: Processed HDF5 dataset path.
        output_dir: Output directory for figures and JSON.
    """
    raise NotImplementedError("Week 12: validate risk map on OOD scenarios")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--data", type=Path, default=Path("data/processed/dataset.h5"))
    parser.add_argument("--output", type=Path, default=Path("results"))
    args = parser.parse_args()

    main(args.checkpoint, args.data, args.output)
