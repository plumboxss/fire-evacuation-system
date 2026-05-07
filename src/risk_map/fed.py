"""
Fractional Effective Dose (FED) accumulation for CO exposure.

Implements Week 12. See docs/manual_v2.md and docs/risk_indicators.md.

Based on Purser's CO dose-response model (SFPE Handbook, 3rd ed.) and
ISO 13571:2012 §7.3 (sensitive population threshold FED = 0.3).
"""
from __future__ import annotations

import numpy as np


def accumulate_fed(
    co_ppm_sequence: np.ndarray,
    dt_seconds: float = 10.0,
    co_exponent: float = 1.036,
) -> np.ndarray:
    """Accumulate FED for CO exposure over a time sequence.

    FED = Σ [CO]^n × Δt / C_t  (Purser model, SFPE Handbook)

    Args:
        co_ppm_sequence: CO concentration in ppm, shape ``(T, ...)``.
                         First axis is time; remaining axes are spatial.
        dt_seconds: Time step between frames in seconds.
        co_exponent: Dose-response exponent n. Default 1.036.

    Returns:
        Cumulative FED array of shape matching spatial dimensions of
        ``co_ppm_sequence`` (i.e., ``co_ppm_sequence.shape[1:]``).
        Values ≥ FED_THRESHOLD (0.3) indicate incapacitation risk.

    Raises:
        ValueError: If ``co_ppm_sequence`` has fewer than 1 time step.
    """
    raise NotImplementedError("Week 12: implement Purser FED accumulation")


def fed_at_time(
    co_ppm_sequence: np.ndarray,
    t_index: int,
    dt_seconds: float = 10.0,
) -> np.ndarray:
    """Return the FED accumulated up to frame ``t_index``.

    Args:
        co_ppm_sequence: ``(T, ...)`` CO concentration in ppm.
        t_index: Frame index (0-based) up to which FED is accumulated.
        dt_seconds: Time step in seconds.

    Returns:
        FED array of shape ``co_ppm_sequence.shape[1:]``.
    """
    raise NotImplementedError("Week 12: accumulate FED up to t_index")


def is_incapacitated(fed: np.ndarray, threshold: float = 0.3) -> np.ndarray:
    """Return boolean mask of cells where FED exceeds the threshold.

    Args:
        fed: FED array, any shape.
        threshold: Incapacitation threshold. Default 0.3 (sensitive population).

    Returns:
        Boolean array, same shape as ``fed``.
    """
    raise NotImplementedError("Week 12: compare FED to threshold")


if __name__ == "__main__":
    print("fed.py — skeleton only (not yet implemented)")
    print("SKIP")
