"""Shared constants, normalization, and geometry utilities."""
from src.shared.constants import (
    GRID_SHAPE,
    DOMAIN_SIZE_M,
    CELL_SIZE_M,
    TIME_STEPS,
    DT_SECONDS,
    T_END_SECONDS,
    N_INPUT_CHANNELS,
    N_OUTPUT_CHANNELS,
    TENABILITY,
    N_CELLS,
)
from src.shared.normalization import (
    normalize_temperature,
    denormalize_temperature,
    normalize_visibility,
    denormalize_visibility,
    normalize_co,
    denormalize_co,
)

__all__ = [
    "GRID_SHAPE",
    "DOMAIN_SIZE_M",
    "CELL_SIZE_M",
    "TIME_STEPS",
    "DT_SECONDS",
    "T_END_SECONDS",
    "N_INPUT_CHANNELS",
    "N_OUTPUT_CHANNELS",
    "TENABILITY",
    "N_CELLS",
    "normalize_temperature",
    "denormalize_temperature",
    "normalize_visibility",
    "denormalize_visibility",
    "normalize_co",
    "denormalize_co",
]
