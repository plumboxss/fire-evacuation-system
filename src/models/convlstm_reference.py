"""
Reference ConvLSTM implementation (2-D, for comparison / transfer).

Implements Week 9–10. See docs/manual_v2.md.

This is a standard 2-D ConvLSTM (Shi et al., 2015) used as a reference
baseline. The project's primary model is the 3-D version in conv_lstm_3d.py.
This module may be used to validate training dynamics on a simpler architecture.
"""
from __future__ import annotations

from typing import List, Optional, Tuple


class ConvLSTMCell2D:
    """Standard 2-D ConvLSTM cell (Shi et al., 2015).

    Args:
        in_channels: Input feature channels.
        hidden_dim: Hidden state channels.
        kernel_size: 2-D kernel size (h, w).
        bias: Use bias in convolutions.
    """

    def __init__(
        self,
        in_channels: int,
        hidden_dim: int,
        kernel_size: Tuple[int, int] = (3, 3),
        bias: bool = True,
    ) -> None:
        raise NotImplementedError("Week 9: implement 2-D ConvLSTMCell reference")

    def forward(self, x, h_prev, c_prev):
        """Single-step cell update.

        Args:
            x: ``(B, in_channels, H, W)``.
            h_prev: ``(B, hidden_dim, H, W)``.
            c_prev: ``(B, hidden_dim, H, W)``.

        Returns:
            ``(h_next, c_next)``, each ``(B, hidden_dim, H, W)``.
        """
        raise NotImplementedError("Week 9: implement ConvLSTMCell2D.forward")


if __name__ == "__main__":
    print("convlstm_reference.py — skeleton only (not yet implemented)")
    print("SKIP")
