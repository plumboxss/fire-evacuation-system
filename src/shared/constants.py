"""
Project-wide numerical constants for the fire evacuation prediction system.

Import from this module everywhere rather than hard-coding values.
All constraints here are fixed for the lifetime of the project — see CLAUDE.md.
"""
from __future__ import annotations

from dataclasses import dataclass

# ── Grid / domain ──────────────────────────────────────────────────────────────
GRID_SHAPE: tuple[int, int, int] = (60, 40, 6)
"""(nx, ny, nz) — number of cells along each axis."""

DOMAIN_SIZE_M: tuple[float, float, float] = (30.0, 20.0, 3.0)
"""Physical domain dimensions in metres (Lx, Ly, Lz)."""

CELL_SIZE_M: float = 0.5
"""Side length of each cubic cell in metres. NEVER change to 0.2."""

# ── Time ───────────────────────────────────────────────────────────────────────
TIME_STEPS: int = 31
"""Number of temporal frames including t=0 (0, 10, 20, …, 300 s)."""

DT_SECONDS: float = 10.0
"""Time between consecutive frames, in seconds."""

T_END_SECONDS: float = 300.0
"""Final simulation time in seconds."""

# ── Model channels ─────────────────────────────────────────────────────────────
N_INPUT_CHANNELS: int = 5
"""Channels fed into the model: [T, V, CO, mask, time_enc]."""

N_OUTPUT_CHANNELS: int = 3
"""Channels produced by the model: [T, V, CO]."""

# ── Scenario split ─────────────────────────────────────────────────────────────
N_SCENARIOS_TOTAL: int = 30
N_SCENARIOS_TRAIN: int = 24
N_SCENARIOS_VAL: int = 3
N_SCENARIOS_OOD: int = 3

# ── Physical reference values (used by normalization.py) ───────────────────────
T_AMBIENT_C: float = 20.0
"""Ambient (pre-fire) temperature in °C — normalization lower bound."""

T_MAX_C: float = 1200.0
"""Maximum expected fire temperature in °C — normalization upper bound."""

V_MAX_M: float = 30.0
"""Smoke-free visibility in metres — normalization upper bound."""

CO_MAX_PPM: float = 5000.0
"""CO normalization ceiling in ppm."""


@dataclass(frozen=True)
class _TenanabilityThresholds:
    """Tenability thresholds from ISO 13571:2012 and the SFPE Handbook."""

    # Temperature (°C)
    T_SAFE_C: float = 30.0
    T_DANGER_C: float = 60.0

    # Visibility (m) — higher means safer
    V_SAFE_M: float = 10.0
    V_DANGER_M: float = 3.0

    # CO instantaneous (ppm)
    CO_SAFE_PPM: float = 100.0
    CO_DANGER_PPM: float = 1400.0

    # FED cumulative threshold (sensitive population, ISO 13571)
    FED_THRESHOLD: float = 0.3


TENABILITY = _TenanabilityThresholds()
"""Tenability thresholds singleton. Access as TENABILITY.T_SAFE_C etc."""

# ── Derived (do not modify) ────────────────────────────────────────────────────
N_CELLS: int = GRID_SHAPE[0] * GRID_SHAPE[1] * GRID_SHAPE[2]
"""Total number of grid cells — must equal 14 400."""


# ── Self-test ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== constants.py self-test ===")
    errors: list[str] = []

    if GRID_SHAPE != (60, 40, 6):
        errors.append(f"GRID_SHAPE wrong: {GRID_SHAPE}")
    if DOMAIN_SIZE_M != (30.0, 20.0, 3.0):
        errors.append(f"DOMAIN_SIZE_M wrong: {DOMAIN_SIZE_M}")
    if abs(CELL_SIZE_M - 0.5) > 1e-9:
        errors.append(f"CELL_SIZE_M wrong: {CELL_SIZE_M}")
    if TIME_STEPS != 31:
        errors.append(f"TIME_STEPS wrong: {TIME_STEPS}")
    if abs(DT_SECONDS - 10.0) > 1e-9:
        errors.append(f"DT_SECONDS wrong: {DT_SECONDS}")
    if abs(T_END_SECONDS - 300.0) > 1e-9:
        errors.append(f"T_END_SECONDS wrong: {T_END_SECONDS}")
    if N_INPUT_CHANNELS != 5:
        errors.append(f"N_INPUT_CHANNELS wrong: {N_INPUT_CHANNELS}")
    if N_OUTPUT_CHANNELS != 3:
        errors.append(f"N_OUTPUT_CHANNELS wrong: {N_OUTPUT_CHANNELS}")

    # Grid product
    nx, ny, nz = GRID_SHAPE
    expected_cells = 14400
    if nx * ny * nz != expected_cells:
        errors.append(
            f"Grid product {nx}*{ny}*{nz} = {nx * ny * nz} != {expected_cells}"
        )
    if N_CELLS != expected_cells:
        errors.append(f"N_CELLS={N_CELLS} != {expected_cells}")

    # Domain / cell_size consistency
    for label, domain_len, n_cells in zip(("X", "Y", "Z"), DOMAIN_SIZE_M, GRID_SHAPE):
        expected_n = round(domain_len / CELL_SIZE_M)
        if expected_n != n_cells:
            errors.append(
                f"{label}: {domain_len}m / {CELL_SIZE_M}m = {expected_n} != {n_cells}"
            )

    # Scenario split sums to total
    split_sum = N_SCENARIOS_TRAIN + N_SCENARIOS_VAL + N_SCENARIOS_OOD
    if split_sum != N_SCENARIOS_TOTAL:
        errors.append(
            f"Scenario split {N_SCENARIOS_TRAIN}+{N_SCENARIOS_VAL}+{N_SCENARIOS_OOD}"
            f" = {split_sum} != {N_SCENARIOS_TOTAL}"
        )

    if errors:
        for e in errors:
            print(f"  FAIL: {e}")
        raise SystemExit(1)

    print(f"  GRID_SHAPE    : {GRID_SHAPE}")
    print(f"  DOMAIN_SIZE   : {DOMAIN_SIZE_M} m")
    print(f"  CELL_SIZE     : {CELL_SIZE_M} m")
    print(f"  N_CELLS       : {N_CELLS}")
    print(f"  TIME_STEPS    : {TIME_STEPS}  ({T_END_SECONDS} s at {DT_SECONDS} s intervals)")
    print(f"  CHANNELS      : in={N_INPUT_CHANNELS}  out={N_OUTPUT_CHANNELS}")
    print(
        f"  TENABILITY    : "
        f"T=[{TENABILITY.T_SAFE_C}, {TENABILITY.T_DANGER_C}] °C  "
        f"V=[{TENABILITY.V_DANGER_M}, {TENABILITY.V_SAFE_M}] m  "
        f"CO=[{TENABILITY.CO_SAFE_PPM}, {TENABILITY.CO_DANGER_PPM}] ppm  "
        f"FED<{TENABILITY.FED_THRESHOLD}"
    )
    print("PASS")
