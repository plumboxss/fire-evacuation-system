"""
Instantaneous tenability functions (ISO 13571 / SFPE Handbook).

Implements Week 12. See docs/manual_v2.md and docs/risk_indicators.md.

Converts normalised fire field values to per-indicator danger scores
in [0, 1], then aggregates them into a single danger score.
"""
from __future__ import annotations

import numpy as np


def temperature_danger(T_norm: np.ndarray) -> np.ndarray:
    """Convert normalised temperature to danger score.

    Maps the safe-to-danger ramp from TENABILITY.T_SAFE_C→T_DANGER_C
    (30–60 °C) to [0, 1] using the raw field values.

    Args:
        T_norm: Normalised temperature array, any shape, values in [0, 1].

    Returns:
        Danger array, same shape, values in [0, 1].
    """
    raise NotImplementedError("Week 12: map normalised T to danger via tenability thresholds")


def visibility_danger(V_norm: np.ndarray) -> np.ndarray:
    """Convert normalised visibility to danger score.

    Visibility is already inversely normalised (0 = safe, 1 = no sight),
    so this function maps the safe-to-danger ramp V_SAFE→V_DANGER
    (10 m → 3 m) to [0, 1].

    Args:
        V_norm: Inverse-normalised visibility array, any shape, values in [0, 1].

    Returns:
        Danger array, same shape, values in [0, 1].
    """
    raise NotImplementedError("Week 12: map normalised V to danger via tenability thresholds")


def co_danger(CO_norm: np.ndarray) -> np.ndarray:
    """Convert normalised CO concentration to danger score.

    Maps the safe-to-danger ramp CO_SAFE→CO_DANGER (100–1400 ppm) to [0, 1].

    Args:
        CO_norm: Normalised CO array, any shape, values in [0, 1].

    Returns:
        Danger array, same shape, values in [0, 1].
    """
    raise NotImplementedError("Week 12: map normalised CO to danger via tenability thresholds")


def aggregate_danger(
    d_T: np.ndarray,
    d_V: np.ndarray,
    d_CO: np.ndarray,
    w_T: float = 0.4,
    w_V: float = 0.4,
    w_CO: float = 0.2,
) -> np.ndarray:
    """Weighted aggregation of per-indicator danger scores.

    Args:
        d_T: Temperature danger, any shape, [0, 1].
        d_V: Visibility danger, same shape, [0, 1].
        d_CO: CO danger, same shape, [0, 1].
        w_T: Temperature weight. Default 0.4.
        w_V: Visibility weight. Default 0.4.
        w_CO: CO weight. Default 0.2.

    Returns:
        Aggregated danger array, same shape, [0, 1].

    Raises:
        ValueError: If weights do not sum to 1.0 (tolerance 1e-6).
    """
    raise NotImplementedError("Week 12: compute weighted sum of danger indicators")


if __name__ == "__main__":
    print("tenability.py — skeleton only (not yet implemented)")
    print("SKIP")
