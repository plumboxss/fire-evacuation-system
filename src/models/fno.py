"""
Fourier Neural Operator (FNO) for fire spread prediction.

Implements Week 11. See docs/manual_v2.md.

Uses the neuraloperator library for the core FNO blocks.
The physics-informed loss terms are in pi_losses.py.

Model specification:
    Input  : (B, 5, 60, 40, 6)   — [T, V, CO, mask, time_enc], normalised
    Output : (B, 3, 60, 40, 6)   — [T, V, CO], normalised
    Config : configs/pi_fno.yaml
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple


class FNOBlock3D:
    """Single Fourier integral operator block (F-layer).

    Applies spectral convolution in the Fourier domain followed by
    a pointwise linear bypass, then a nonlinearity.

    Args:
        in_channels: Input channel width.
        out_channels: Output channel width.
        modes: Fourier truncation modes ``(mx, my, mz)``.
        activation: Nonlinearity name: ``"gelu"`` or ``"relu"``.
    """

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        modes: Tuple[int, int, int] = (8, 8, 4),
        activation: str = "gelu",
    ) -> None:
        raise NotImplementedError("Week 11: implement FNOBlock3D using neuraloperator")

    def forward(self, x):
        """Apply one FNO block.

        Args:
            x: ``(B, in_channels, 60, 40, 6)``.

        Returns:
            ``(B, out_channels, 60, 40, 6)``.
        """
        raise NotImplementedError("Week 11: implement FNOBlock3D.forward")


class PIFNO(object):
    """Physics-Informed FNO for 3-D fire field prediction.

    Stacks ``n_layers`` FNO blocks with a lifting layer (in → width)
    and a projection layer (width → out_channels).

    Args:
        in_channels: 5 — [T, V, CO, mask, time_enc].
        out_channels: 3 — [T, V, CO].
        modes: Fourier truncation modes per spatial dimension.
        width: Internal channel width.
        n_layers: Number of FNO blocks.
        activation: Pointwise nonlinearity.
    """

    def __init__(
        self,
        in_channels: int = 5,
        out_channels: int = 3,
        modes: Tuple[int, int, int] = (8, 8, 4),
        width: int = 32,
        n_layers: int = 4,
        activation: str = "gelu",
    ) -> None:
        raise NotImplementedError("Week 11: build PIFNO with lifting + FNO blocks + projection")

    def forward(self, x):
        """Single forward pass.

        Args:
            x: ``(B, 5, 60, 40, 6)``, float32, values in [0, 1].

        Returns:
            ``(B, 3, 60, 40, 6)``, float32, values in [0, 1].
        """
        raise NotImplementedError("Week 11: implement PIFNO.forward")

    def get_config(self) -> Dict[str, Any]:
        """Return hyperparameter dict for W&B logging.

        Returns:
            Dict with keys: in_channels, out_channels, modes, width,
            n_layers, activation.
        """
        raise NotImplementedError("Week 11: implement get_config")


if __name__ == "__main__":
    print("fno.py — skeleton only (not yet implemented)")
    print("SKIP")
