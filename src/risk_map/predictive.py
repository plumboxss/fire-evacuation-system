"""
PredictiveRiskMap: live model inference + caching for path planning.

Implements Week 12. See docs/manual_v2.md.

Unlike StaticRiskMap, this class runs the model forward pass on demand
and caches the result per time step, enabling real-time re-planning.
"""
from __future__ import annotations

import numpy as np

from src.risk_map.risk_map_class import RiskMap


class PredictiveRiskMap(RiskMap):
    """Risk map that runs live model inference with frame-level caching.

    Args:
        model: A trained ConvLSTM3D or PIFNO instance with a ``forward`` method.
        current_input: Current normalised input frame ``(5, 60, 40, 6)``.
        device: PyTorch device string (``"cuda"`` or ``"cpu"``).

    Notes:
        Predictions are cached: calling ``query`` at the same ``t`` multiple
        times only runs inference once.
    """

    def __init__(
        self,
        model,
        current_input: np.ndarray,
        device: str = "cuda",
    ) -> None:
        raise NotImplementedError("Week 12: initialise PredictiveRiskMap with model and cache")

    def query(self, xyz: np.ndarray, t: float | None = None) -> float:
        """Query danger at a world coordinate, running inference if needed.

        Args:
            xyz: ``[x_m, y_m, z_m]``.
            t: Query time in seconds.

        Returns:
            Danger ∈ [0, 1]. Returns 1.0 for out-of-bounds.
        """
        raise NotImplementedError("Week 12: lookup cached prediction or run model")

    def update(self, new_input: np.ndarray) -> None:
        """Update the current input frame and invalidate the prediction cache.

        Args:
            new_input: New normalised input frame ``(5, 60, 40, 6)``.
        """
        raise NotImplementedError("Week 12: update input and clear cache")


if __name__ == "__main__":
    print("predictive.py — skeleton only (not yet implemented)")
    print("SKIP")
