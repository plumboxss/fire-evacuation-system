"""
Training callbacks: checkpointing, early stopping, W&B logging.

Implements Week 9–11 training. See docs/manual_v2.md.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional


class CheckpointCallback:
    """Save model checkpoints when validation loss improves.

    Args:
        dirpath: Directory for checkpoint files.
        filename: Checkpoint filename template (e.g. ``"epoch={epoch}-val={val_loss:.4f}"``).
        monitor: Metric to monitor. Default ``"val/loss"``.
        mode: ``"min"`` to save on decrease, ``"max"`` on increase.
        save_top_k: Keep only the best k checkpoints.
    """

    def __init__(
        self,
        dirpath: Path,
        filename: str = "best",
        monitor: str = "val/loss",
        mode: str = "min",
        save_top_k: int = 3,
    ) -> None:
        raise NotImplementedError("Week 9: implement CheckpointCallback")

    def on_validation_end(self, epoch: int, metrics: dict) -> None:
        """Called after each validation epoch.

        Args:
            epoch: Current epoch number (0-indexed).
            metrics: Dict of metric name → scalar value.
        """
        raise NotImplementedError("Week 9: check if checkpoint should be saved")


class EarlyStoppingCallback:
    """Stop training when validation loss stops improving.

    Args:
        monitor: Metric to monitor.
        patience: Epochs without improvement before stopping.
        min_delta: Minimum change to count as improvement.
        mode: ``"min"`` or ``"max"``.
    """

    def __init__(
        self,
        monitor: str = "val/loss",
        patience: int = 15,
        min_delta: float = 1e-5,
        mode: str = "min",
    ) -> None:
        raise NotImplementedError("Week 9: implement EarlyStoppingCallback")

    def should_stop(self, epoch: int, metrics: dict) -> bool:
        """Return True if training should be stopped.

        Args:
            epoch: Current epoch.
            metrics: Current metric values.

        Returns:
            True if patience is exhausted.
        """
        raise NotImplementedError("Week 9: implement patience counter")


class WandBCallback:
    """Log training metrics and model config to Weights & Biases.

    Args:
        project: W&B project name.
        config: Model and training hyperparameters to log.
        tags: Optional list of run tags.
    """

    def __init__(
        self,
        project: str,
        config: dict,
        tags: Optional[list[str]] = None,
    ) -> None:
        raise NotImplementedError("Week 9: initialise W&B run")

    def log(self, metrics: dict, step: int) -> None:
        """Log a dict of scalar metrics.

        Args:
            metrics: Name → value mapping.
            step: Global training step.
        """
        raise NotImplementedError("Week 9: call wandb.log")

    def finish(self) -> None:
        """Close the W&B run."""
        raise NotImplementedError("Week 9: call wandb.finish")


if __name__ == "__main__":
    print("callbacks.py — skeleton only (not yet implemented)")
    print("SKIP")
