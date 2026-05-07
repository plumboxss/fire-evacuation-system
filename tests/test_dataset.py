"""
Tests for src/dataset/fire_dataset.py and src/dataset/data_module.py.

Implements Week 7–8 tests. See docs/manual_v2.md.
Fill in test bodies when FireDataset is implemented.
"""
from __future__ import annotations

import pytest


class TestFireDataset:
    def test_len_train_split(self) -> None:
        """Training split should have 24 × 30 = 720 samples."""
        raise NotImplementedError("Week 7: implement after FireDataset is ready")

    def test_getitem_shapes(self) -> None:
        """Each item should be (x, y) with shapes (5, 60, 40, 6) and (3, 60, 40, 6)."""
        raise NotImplementedError("Week 7: verify __getitem__ output shapes")

    def test_values_in_unit_interval(self) -> None:
        """All tensor values should be in [0, 1]."""
        raise NotImplementedError("Week 7: check normalised range")

    def test_invalid_split_raises(self) -> None:
        """Passing an unknown split name should raise ValueError."""
        raise NotImplementedError("Week 7: verify ValueError on bad split")


class TestFireDataModule:
    def test_dataloaders_exist(self) -> None:
        """All three dataloaders should be non-None."""
        raise NotImplementedError("Week 7: implement after FireDataModule is ready")

    def test_batch_shapes(self) -> None:
        """First batch should have shapes (B, 5, 60, 40, 6) and (B, 3, 60, 40, 6)."""
        raise NotImplementedError("Week 7: check batch tensor shapes")
