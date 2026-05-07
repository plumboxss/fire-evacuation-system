"""
PyTorch Dataset for fire simulation scenarios.

Implements Week 7–8 dataset. See docs/manual_v2.md.

Loads pairs of (input_frame, target_frame) from the processed HDF5 dataset.
Each sample represents one temporal step: model predicts frame t+1 from frame t.
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal

import numpy as np


class FireDataset:
    """PyTorch Dataset wrapping the processed fire simulation HDF5 file.

    Each item is a (input, target) pair of normalised tensors:
        input  : shape (5, 60, 40, 6) — channels [T, V, CO, mask, time_enc]
        target : shape (3, 60, 40, 6) — channels [T, V, CO]

    Args:
        dataset_path: Path to ``data/processed/dataset.h5``.
        split: One of ``"train"``, ``"val"``, or ``"ood"``.
        augment: If True, apply random horizontal flips during training.

    Raises:
        FileNotFoundError: If ``dataset_path`` does not exist.
        ValueError: If ``split`` is not one of the accepted values.
    """

    def __init__(
        self,
        dataset_path: Path,
        split: Literal["train", "val", "ood"] = "train",
        augment: bool = False,
    ) -> None:
        raise NotImplementedError("Week 7: implement FireDataset.__init__")

    def __len__(self) -> int:
        """Return total number of (input, target) pairs in this split.

        Returns:
            Number of frame pairs = n_scenarios_in_split × (TIME_STEPS − 1).
        """
        raise NotImplementedError("Week 7: implement __len__")

    def __getitem__(self, idx: int):
        """Return the idx-th (input, target) tensor pair.

        Args:
            idx: Sample index in [0, len(self)).

        Returns:
            Tuple ``(x, y)`` where:
                x: ``torch.Tensor`` of shape ``(5, 60, 40, 6)``, float32.
                y: ``torch.Tensor`` of shape ``(3, 60, 40, 6)``, float32.

        Raises:
            IndexError: If ``idx`` is out of range.
        """
        raise NotImplementedError("Week 7: implement __getitem__")


if __name__ == "__main__":
    print("fire_dataset.py — skeleton only (not yet implemented)")
    print("SKIP")
