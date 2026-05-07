"""
Experiment: Compare static vs dynamic (re-planned) evacuation paths.

Implements Week 12 experiment. See docs/manual_v2.md.

Simulates evacuation from 5 fixed start positions for each OOD scenario,
comparing: (1) shortest-distance path, (2) static risk-weighted A*,
and (3) dynamic A* with re-planning every 10 s.

Usage:
    python experiments/exp_path_001_compare_paths.py \\
        --checkpoint checkpoints/pi_fno/best.pt
"""
from __future__ import annotations

from pathlib import Path


def main(
    checkpoint_path: Path,
    dataset_path: Path = Path("data/processed/dataset.h5"),
    output_dir: Path = Path("results"),
) -> None:
    """Run the path planning comparison experiment.

    Args:
        checkpoint_path: Trained model checkpoint.
        dataset_path: Processed HDF5 dataset path.
        output_dir: Output directory.
    """
    raise NotImplementedError("Week 12: compare evacuation path strategies")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--data", type=Path, default=Path("data/processed/dataset.h5"))
    parser.add_argument("--output", type=Path, default=Path("results"))
    args = parser.parse_args()

    main(args.checkpoint, args.data, args.output)
