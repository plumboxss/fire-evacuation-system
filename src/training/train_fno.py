"""
Training entry point for the PI-FNO model.

Implements Week 11. See docs/manual_v2.md.

Usage:
    python -m src.training.train_fno --config configs/pi_fno.yaml
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional


def train(
    config_path: Path = Path("configs/pi_fno.yaml"),
    dataset_path: Path = Path("data/processed/dataset.h5"),
    checkpoint_dir: Optional[Path] = None,
    resume_from: Optional[Path] = None,
) -> None:
    """Train a PI-FNO model with settings from ``config_path``.

    Loads the physics-informed loss weights from ``config_path →
    training.loss_weights`` and passes them to
    :func:`src.models.pi_losses.combined_pi_loss`.

    Args:
        config_path: Path to ``configs/pi_fno.yaml``.
        dataset_path: Path to the processed HDF5 dataset.
        checkpoint_dir: Where to save checkpoints. Defaults to
                        ``checkpoints/pi_fno/``.
        resume_from: Optional checkpoint path to resume from.

    Raises:
        FileNotFoundError: If ``config_path`` or ``dataset_path`` is missing.
    """
    raise NotImplementedError("Week 11: wire up PIFNO → combined_pi_loss → Trainer → W&B")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train PI-FNO model")
    parser.add_argument("--config", type=Path, default=Path("configs/pi_fno.yaml"))
    parser.add_argument("--data", type=Path, default=Path("data/processed/dataset.h5"))
    parser.add_argument("--resume", type=Path, default=None)
    args = parser.parse_args()

    train(config_path=args.config, dataset_path=args.data, resume_from=args.resume)
