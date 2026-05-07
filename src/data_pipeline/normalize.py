"""
Apply channel-wise normalisation to raw FDS field arrays.

Implements Week 5–6 data pipeline. See docs/manual_v2.md.

Wraps the normalization functions from src/shared/normalization.py
and applies them to full (31, 60, 40, 6) scenario arrays.
"""
from __future__ import annotations

from typing import Dict

import numpy as np


def normalize_scenario(
    raw_fields: Dict[str, np.ndarray],
) -> Dict[str, np.ndarray]:
    """Apply normalisation to all field variables in a scenario.

    Args:
        raw_fields: Dict with keys ``"temperature"``, ``"visibility"``,
                    ``"co_ppm"``. Each value shape: ``(31, 60, 40, 6)``,
                    in physical units (°C, m, ppm).

    Returns:
        Dict with the same keys. Each value shape: ``(31, 60, 40, 6)``,
        normalised to ``[0, 1]`` using rules from
        :mod:`src.shared.normalization`.

    Raises:
        ValueError: If any input array has unexpected shape.
    """
    raise NotImplementedError("Week 6: apply normalization to scenario arrays")


def build_input_tensor(
    normalised: Dict[str, np.ndarray],
    mask: np.ndarray,
) -> np.ndarray:
    """Stack normalised fields + mask + time encoding into the model input format.

    Args:
        normalised: Dict with keys ``"temperature"``, ``"visibility"``,
                    ``"co_ppm"``. Each shape: ``(31, 60, 40, 6)``.
        mask: Boolean or float array of shape ``(60, 40, 6)``.
              1.0 = fluid cell, 0.0 = solid.

    Returns:
        Input tensor of shape ``(31, 5, 60, 40, 6)``.
        Channel order: [T, V, CO, mask, time_enc].

    Raises:
        ValueError: If input shapes are inconsistent.
    """
    raise NotImplementedError("Week 6: stack channels into (31, 5, 60, 40, 6)")


if __name__ == "__main__":
    print("normalize.py — skeleton only (not yet implemented)")
    print("SKIP")
