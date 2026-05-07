"""
Generic training loop used by both ConvLSTM and PI-FNO.

Implements Week 9–11 training. See docs/manual_v2.md.

Handles the train/val epoch loop, gradient clipping, LR scheduling,
and callback dispatch. Model-specific concerns (loss computation) are
delegated to the caller via a loss_fn argument.
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional


class Trainer:
    """Epoch-loop trainer for fire prediction models.

    Args:
        model: A ConvLSTM3D or PIFNO instance.
        optimizer: Configured PyTorch optimiser.
        scheduler: Optional LR scheduler.
        loss_fn: Callable ``(pred, target) → scalar loss``.
        device: ``"cuda"`` or ``"cpu"``.
        max_epochs: Maximum number of training epochs.
        grad_clip: Gradient norm clipping threshold.
        callbacks: List of callback objects (CheckpointCallback, etc.).
    """

    def __init__(
        self,
        model,
        optimizer,
        loss_fn: Callable,
        device: str = "cuda",
        max_epochs: int = 100,
        grad_clip: float = 1.0,
        scheduler=None,
        callbacks: Optional[list] = None,
    ) -> None:
        raise NotImplementedError("Week 9: implement Trainer.__init__")

    def fit(self, train_loader, val_loader) -> dict:
        """Run the full training loop.

        Args:
            train_loader: DataLoader for the training split.
            val_loader: DataLoader for the validation split.

        Returns:
            Dict with keys ``"train_losses"``, ``"val_losses"`` —
            lists of per-epoch scalar losses.
        """
        raise NotImplementedError("Week 9: implement epoch loop")

    def train_epoch(self, loader) -> float:
        """Run one training epoch.

        Args:
            loader: Training DataLoader.

        Returns:
            Mean training loss for the epoch.
        """
        raise NotImplementedError("Week 9: implement train_epoch")

    def val_epoch(self, loader) -> float:
        """Run one validation epoch (no gradient computation).

        Args:
            loader: Validation DataLoader.

        Returns:
            Mean validation loss for the epoch.
        """
        raise NotImplementedError("Week 9: implement val_epoch")


if __name__ == "__main__":
    print("trainer.py — skeleton only (not yet implemented)")
    print("SKIP")
