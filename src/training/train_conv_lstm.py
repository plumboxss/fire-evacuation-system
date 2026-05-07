"""
Training entry point for the ConvLSTM3D model.

Implements Week 9–10. See docs/manual_v2.md.

Usage:
    python -m src.training.train_conv_lstm --config configs/conv_lstm.yaml
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional


def train(
    config_path: Path = Path("configs/conv_lstm.yaml"),
    dataset_path: Path = Path("data/processed/dataset.h5"),
    checkpoint_dir: Optional[Path] = None,
    resume_from: Optional[Path] = None,
) -> None:
    """Train a ConvLSTM3D model with settings from ``config_path``.

    Args:
        config_path: Path to ``configs/conv_lstm.yaml``.
        dataset_path: Path to the processed HDF5 dataset.
        checkpoint_dir: Where to save checkpoints. Defaults to
                        ``checkpoints/conv_lstm/``.
        resume_from: Optional checkpoint path to resume from.

    Raises:
        FileNotFoundError: If ``config_path`` or ``dataset_path`` is missing.
    """
    raise NotImplementedError("Week 9: wire up ConvLSTM3D → Trainer → W&B")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train ConvLSTM3D model")
    parser.add_argument("--config", type=Path, default=Path("configs/conv_lstm.yaml"))
    parser.add_argument("--data", type=Path, default=Path("data/processed/dataset.h5"))
    parser.add_argument("--resume", type=Path, default=None)
    args = parser.parse_args()

    train(config_path=args.config, dataset_path=args.data, resume_from=args.resume)
