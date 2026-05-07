"""
Bidirectional normalization for fire field variables.

All model inputs/outputs are normalised to [0, 1] where higher values
indicate greater danger. Visibility uses an inverse mapping (low visibility
= high normalised value).

Normalization rules
-------------------
Temperature : ``(T_celsius − 20) / 1180``  →  clip [0, 1]
Visibility  : ``1 − clip(V_m / 30, 0, 1)``   (INVERSE: 0 m → 1.0, 30 m → 0.0)
CO          : ``log1p(ppm) / log1p(5000)``  →  clip [0, 1]

Each function accepts and returns numpy arrays of any shape.
"""
from __future__ import annotations

import math

import numpy as np

from src.shared.constants import CO_MAX_PPM, T_AMBIENT_C, T_MAX_C, V_MAX_M

# ── Pre-computed scalars ───────────────────────────────────────────────────────
_T_RANGE: float = T_MAX_C - T_AMBIENT_C        # 1180.0
_LOG_CO_MAX: float = math.log1p(CO_MAX_PPM)    # log1p(5000) ≈ 8.517


# ── Temperature ───────────────────────────────────────────────────────────────

def normalize_temperature(raw: np.ndarray) -> np.ndarray:
    """Normalise temperature from Celsius to [0, 1].

    Mapping: 20 °C → 0.0, 1200 °C → 1.0.
    Values below 20 °C are clipped to 0.0; above 1200 °C to 1.0.

    Args:
        raw: Temperature in degrees Celsius. Any shape.

    Returns:
        Normalised array, same shape as ``raw``, dtype float64, ∈ [0, 1].
    """
    raw = np.asarray(raw, dtype=np.float64)
    return np.clip((raw - T_AMBIENT_C) / _T_RANGE, 0.0, 1.0)


def denormalize_temperature(normalized: np.ndarray) -> np.ndarray:
    """Invert :func:`normalize_temperature`.

    Args:
        normalized: Array with values in [0, 1]. Any shape.

    Returns:
        Temperature in degrees Celsius. Values outside [0, 1] are
        linearly extrapolated without clipping.
    """
    normalized = np.asarray(normalized, dtype=np.float64)
    return normalized * _T_RANGE + T_AMBIENT_C


# ── Visibility ────────────────────────────────────────────────────────────────

def normalize_visibility(raw: np.ndarray) -> np.ndarray:
    """Normalise visibility from metres to [0, 1] with INVERSE mapping.

    High visibility (safe)     → low normalised value (0.0 at 30 m).
    Low  visibility (dangerous) → high normalised value (1.0 at 0 m).

    Args:
        raw: Visibility in metres. Any shape. Negative values treated as 0.

    Returns:
        Normalised array, same shape as ``raw``, dtype float64, ∈ [0, 1].
    """
    raw = np.asarray(raw, dtype=np.float64)
    return 1.0 - np.clip(raw / V_MAX_M, 0.0, 1.0)


def denormalize_visibility(normalized: np.ndarray) -> np.ndarray:
    """Invert :func:`normalize_visibility`.

    Args:
        normalized: Array with values in [0, 1]. Any shape.

    Returns:
        Visibility in metres. Values outside [0, 1] extrapolated linearly.
    """
    normalized = np.asarray(normalized, dtype=np.float64)
    return (1.0 - normalized) * V_MAX_M


# ── CO concentration ──────────────────────────────────────────────────────────

def normalize_co(raw: np.ndarray) -> np.ndarray:
    """Normalise CO concentration from ppm to [0, 1] on a log scale.

    Mapping: 0 ppm → 0.0, 5000 ppm → 1.0.
    Log scale compresses the long tail of high concentrations.

    Args:
        raw: CO concentration in ppm. Any shape. Negative values treated as 0.

    Returns:
        Normalised array, same shape as ``raw``, dtype float64, ∈ [0, 1].
    """
    raw = np.asarray(raw, dtype=np.float64)
    return np.clip(np.log1p(np.maximum(raw, 0.0)) / _LOG_CO_MAX, 0.0, 1.0)


def denormalize_co(normalized: np.ndarray) -> np.ndarray:
    """Invert :func:`normalize_co`.

    Args:
        normalized: Array with values in [0, 1]. Any shape.

    Returns:
        CO concentration in ppm. Input is clipped to [0, 1] before inversion
        to avoid numerical overflow from ``expm1``.
    """
    normalized = np.asarray(normalized, dtype=np.float64)
    return np.expm1(np.clip(normalized, 0.0, 1.0) * _LOG_CO_MAX)


# ── Self-test ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== normalization.py self-test ===")
    errors: list[str] = []
    tol = 1e-9

    # --- Temperature ---
    test_temps = [20.0, 100.0, 600.0, 1200.0]
    for t in test_temps:
        arr = np.array([t])
        recovered = float(denormalize_temperature(normalize_temperature(arr))[0])
        if abs(recovered - t) > tol:
            errors.append(f"T round-trip: {t} °C → {recovered}")

    # Boundary: 0 °C should clip to normalised 0.0
    if float(normalize_temperature(np.array([0.0]))[0]) != 0.0:
        errors.append("T: 0 °C should normalise to 0.0 (clipped)")

    # Monotonicity
    t_vals = np.array([20.0, 100.0, 600.0, 1200.0])
    normed_t = normalize_temperature(t_vals)
    if not (np.diff(normed_t) > 0).all():
        errors.append("T normalisation not strictly increasing")

    # --- Visibility ---
    test_vis = [0.0, 3.0, 10.0, 30.0]
    for v in test_vis:
        arr = np.array([v])
        recovered = float(denormalize_visibility(normalize_visibility(arr))[0])
        if abs(recovered - v) > tol:
            errors.append(f"V round-trip: {v} m → {recovered}")

    # Inverse: high visibility → low normalised value
    if not (normalize_visibility(np.array([30.0]))[0] < normalize_visibility(np.array([0.0]))[0]):
        errors.append("V: 30 m should have lower normalised value than 0 m")

    # --- CO ---
    test_co = [0.0, 100.0, 1000.0, 5000.0]
    for ppm in test_co:
        arr = np.array([ppm])
        recovered = float(denormalize_co(normalize_co(arr))[0])
        if abs(recovered - ppm) > tol:
            errors.append(f"CO round-trip: {ppm} ppm → {recovered}")

    # Boundary: negative ppm treated as 0
    if float(normalize_co(np.array([-100.0]))[0]) != 0.0:
        errors.append("CO: negative ppm should normalise to 0.0")

    if errors:
        for e in errors:
            print(f"  FAIL: {e}")
        raise SystemExit(1)

    print(
        f"  Temperature : 20 °C → {normalize_temperature(np.array([20.0]))[0]:.3f}, "
        f"1200 °C → {normalize_temperature(np.array([1200.0]))[0]:.3f}  [round-trip OK]"
    )
    print(
        f"  Visibility  : 30 m → {normalize_visibility(np.array([30.0]))[0]:.3f}, "
        f"0 m → {normalize_visibility(np.array([0.0]))[0]:.3f}  [round-trip OK, inverse]"
    )
    print(
        f"  CO          : 0 ppm → {normalize_co(np.array([0.0]))[0]:.3f}, "
        f"5000 ppm → {normalize_co(np.array([5000.0]))[0]:.3f}  [round-trip OK, log-scale]"
    )
    print("PASS")
