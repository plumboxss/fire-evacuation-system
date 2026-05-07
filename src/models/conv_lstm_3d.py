"""
ConvLSTM 3D model for fire spread prediction.

Implements Week 9–10. See docs/manual_v2.md.

NOTE: The user has a working ConvLSTM implementation. This file is a
placeholder skeleton. Replace the function bodies with the user's
working version during Week 9, preserving the interface signatures below.

Model specification:
    Input  : (B, 5, 60, 40, 6)   — [T, V, CO, mask, time_enc], normalised
    Output : (B, 3, 60, 40, 6)   — [T, V, CO], normalised
    Config : configs/conv_lstm.yaml
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np


class ConvLSTMCell3D:
    """Single 3-D ConvLSTM cell.

    Args:
        in_channels: Number of input feature channels.
        hidden_dim: Number of hidden state channels.
        kernel_size: 3-D convolution kernel size as (kx, ky, kz).
        bias: Include bias in convolutions.
    """

    def __init__(
        self,
        in_channels: int,
        hidden_dim: int,
        kernel_size: Tuple[int, int, int] = (3, 3, 3),
        bias: bool = True,
    ) -> None:
        raise NotImplementedError("Week 9: implement ConvLSTMCell3D")

    def forward(self, x, h_prev, c_prev):
        """Single-step forward pass.

        Args:
            x: Input of shape ``(B, in_channels, nx, ny, nz)``.
            h_prev: Previous hidden state ``(B, hidden_dim, nx, ny, nz)``.
            c_prev: Previous cell state ``(B, hidden_dim, nx, ny, nz)``.

        Returns:
            Tuple ``(h_next, c_next)``, each ``(B, hidden_dim, nx, ny, nz)``.
        """
        raise NotImplementedError("Week 9: implement ConvLSTMCell3D.forward")


class ConvLSTM3D:
    """Stacked 3-D ConvLSTM for spatiotemporal fire field prediction.

    Args:
        in_channels: 5 — [T, V, CO, mask, time_enc].
        out_channels: 3 — [T, V, CO].
        hidden_dim: Hidden state channels per layer.
        kernel_size: 3-D convolution kernel size.
        num_layers: Number of stacked ConvLSTM layers.
        dropout: Dropout probability between layers.
        batch_norm: Apply batch normalisation after each layer.
    """

    def __init__(
        self,
        in_channels: int = 5,
        out_channels: int = 3,
        hidden_dim: int = 32,
        kernel_size: Tuple[int, int, int] = (3, 3, 3),
        num_layers: int = 2,
        dropout: float = 0.1,
        batch_norm: bool = True,
    ) -> None:
        raise NotImplementedError("Week 9: initialise ConvLSTM3D layers")

    def forward(self, x):
        """Single-step forward pass.

        Args:
            x: Input tensor ``(B, 5, 60, 40, 6)``, float32, values in [0, 1].

        Returns:
            Output tensor ``(B, 3, 60, 40, 6)``, float32, values in [0, 1].
        """
        raise NotImplementedError("Week 9: implement ConvLSTM3D.forward")

    def get_config(self) -> Dict[str, Any]:
        """Return hyperparameter dict for logging.

        Returns:
            Dict with keys: in_channels, out_channels, hidden_dim,
            kernel_size, num_layers, dropout, batch_norm.
        """
        raise NotImplementedError("Week 9: implement get_config")


if __name__ == "__main__":
    print("conv_lstm_3d.py — skeleton only (not yet implemented)")
    print("SKIP")
