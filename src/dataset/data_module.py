"""
DataModule wrapping train/val/OOD FireDataset instances.

Implements Week 7–8 dataset. See docs/manual_v2.md.

Provides PyTorch DataLoader objects configured for the A100 GPU.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional


class FireDataModule:
    """Manages train, validation, and OOD DataLoaders.

    Args:
        dataset_path: Path to ``data/processed/dataset.h5``.
        batch_size: Samples per batch. Default 4 (A100 memory budget).
        num_workers: DataLoader worker processes. Default 4.
        pin_memory: If True, pin memory for faster GPU transfers. Default True.
        augment_train: Apply random augmentation to training data. Default False.

    Raises:
        FileNotFoundError: If ``dataset_path`` does not exist.
    """

    def __init__(
        self,
        dataset_path: Path,
        batch_size: int = 4,
        num_workers: int = 4,
        pin_memory: bool = True,
        augment_train: bool = False,
    ) -> None:
        raise NotImplementedError("Week 7: implement FireDataModule.__init__")

    def train_dataloader(self):
        """Return the training DataLoader.

        Returns:
            ``torch.utils.data.DataLoader`` over the training split.
            Shuffled, ``batch_size`` samples per batch.
        """
        raise NotImplementedError("Week 7: implement train_dataloader")

    def val_dataloader(self):
        """Return the validation DataLoader.

        Returns:
            ``torch.utils.data.DataLoader`` over the val split.
            Not shuffled.
        """
        raise NotImplementedError("Week 7: implement val_dataloader")

    def ood_dataloader(self):
        """Return the OOD evaluation DataLoader.

        Returns:
            ``torch.utils.data.DataLoader`` over the OOD split.
            Not shuffled.
        """
        raise NotImplementedError("Week 7: implement ood_dataloader")


if __name__ == "__main__":
    print("data_module.py — skeleton only (not yet implemented)")
    print("SKIP")
