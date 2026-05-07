"""
Convert model output tensors to danger arrays.

Implements Week 12. See docs/manual_v2.md.

Bridges the model output ``(B, 3, 60, 40, 6)`` to the
``StaticRiskMap`` expected by the path planner.
"""
from __future__ import annotations

import numpy as np

from src.risk_map.risk_map_class import StaticRiskMap


def prediction_to_danger(
    model_output: np.ndarray,
    times: np.ndarray,
    w_T: float = 0.4,
    w_V: float = 0.4,
    w_CO: float = 0.2,
) -> np.ndarray:
    """Convert model output sequence to a per-frame danger array.

    Applies tenability functions from :mod:`src.risk_map.tenability`
    to each time step.

    Args:
        model_output: ``(T, 3, 60, 40, 6)`` — T frames of model predictions,
                      normalised [0, 1]. Channel order: [T, V, CO].
        times: 1-D array of frame times in seconds, length T.
        w_T: Temperature danger weight.
        w_V: Visibility danger weight.
        w_CO: CO danger weight.

    Returns:
        Danger array of shape ``(T, 60, 40, 6)``, values in [0, 1].

    Raises:
        ValueError: If ``model_output.shape[1] != 3``.
        ValueError: If ``model_output.shape[0] != len(times)``.
    """
    raise NotImplementedError("Week 12: apply tenability functions channel-wise")


def build_static_risk_map(
    model_output: np.ndarray,
    times: np.ndarray,
) -> StaticRiskMap:
    """Build a StaticRiskMap from a sequence of model predictions.

    Args:
        model_output: ``(T, 3, 60, 40, 6)`` model prediction sequence.
        times: Frame times in seconds, length T.

    Returns:
        :class:`StaticRiskMap` ready for path planning queries.
    """
    raise NotImplementedError("Week 12: convert model output → danger array → StaticRiskMap")


if __name__ == "__main__":
    print("converter.py — skeleton only (not yet implemented)")
    print("SKIP")
