"""
Abstract base class for all fire prediction models.

Implements Week 9 model framework. See docs/manual_v2.md.

Defines the common interface (forward, predict, count_params) so that
training loops and evaluators can use ConvLSTM and PI-FNO interchangeably.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict


class FirePredictionModel(ABC):
    """Abstract base for ConvLSTM3D and PI-FNO models.

    All concrete models must implement :meth:`forward` and
    :meth:`get_config`.

    Input tensor  : ``(B, 5, 60, 40, 6)``  — see docs/interface_contracts.md
    Output tensor : ``(B, 3, 60, 40, 6)``
    """

    @abstractmethod
    def forward(self, x):
        """Run a single forward pass.

        Args:
            x: Input tensor of shape ``(B, 5, 60, 40, 6)``, float32,
               values normalised to ``[0, 1]``.

        Returns:
            Output tensor of shape ``(B, 3, 60, 40, 6)``, float32,
            values normalised to ``[0, 1]``.
        """
        raise NotImplementedError

    @abstractmethod
    def get_config(self) -> Dict[str, Any]:
        """Return a serialisable dict of model hyperparameters.

        Returns:
            Dictionary suitable for logging to W&B or saving as YAML.
        """
        raise NotImplementedError

    def count_parameters(self) -> int:
        """Return total number of trainable parameters.

        Returns:
            Integer count of parameters with ``requires_grad=True``.
        """
        raise NotImplementedError("Week 9: implement parameter counting")

    def save(self, path: Path) -> None:
        """Serialise model weights to ``path``.

        Args:
            path: Destination ``.pt`` or ``.pth`` file path.
        """
        raise NotImplementedError("Week 9: implement model saving")

    @classmethod
    def load(cls, path: Path) -> "FirePredictionModel":
        """Load model weights from ``path``.

        Args:
            path: Path to a checkpoint file saved by :meth:`save`.

        Returns:
            Instantiated model with weights loaded.

        Raises:
            FileNotFoundError: If ``path`` does not exist.
        """
        raise NotImplementedError("Week 9: implement model loading")


if __name__ == "__main__":
    print("base.py — skeleton only (not yet implemented)")
    print("SKIP")
