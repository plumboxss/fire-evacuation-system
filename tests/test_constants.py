"""
Tests for src/shared/constants.py — Tier 1 (must pass from day 1).
"""
import pytest

from src.shared.constants import (
    CELL_SIZE_M,
    CO_MAX_PPM,
    DOMAIN_SIZE_M,
    DT_SECONDS,
    GRID_SHAPE,
    N_CELLS,
    N_INPUT_CHANNELS,
    N_OUTPUT_CHANNELS,
    N_SCENARIOS_OOD,
    N_SCENARIOS_TOTAL,
    N_SCENARIOS_TRAIN,
    N_SCENARIOS_VAL,
    T_AMBIENT_C,
    T_END_SECONDS,
    T_MAX_C,
    TENABILITY,
    TIME_STEPS,
    V_MAX_M,
)


class TestGridShape:
    def test_shape_values(self) -> None:
        assert GRID_SHAPE == (60, 40, 6)

    def test_shape_is_tuple(self) -> None:
        assert isinstance(GRID_SHAPE, tuple)
        assert len(GRID_SHAPE) == 3

    def test_grid_product_equals_14400(self) -> None:
        nx, ny, nz = GRID_SHAPE
        assert nx * ny * nz == 14400

    def test_n_cells_equals_14400(self) -> None:
        assert N_CELLS == 14400

    def test_n_cells_matches_shape_product(self) -> None:
        assert N_CELLS == GRID_SHAPE[0] * GRID_SHAPE[1] * GRID_SHAPE[2]


class TestDomainConsistency:
    def test_domain_size(self) -> None:
        assert DOMAIN_SIZE_M == (30.0, 20.0, 3.0)

    def test_cell_size(self) -> None:
        assert abs(CELL_SIZE_M - 0.5) < 1e-12

    def test_domain_divided_by_cell_equals_grid(self) -> None:
        for domain_len, n in zip(DOMAIN_SIZE_M, GRID_SHAPE):
            assert abs(domain_len / CELL_SIZE_M - n) < 1e-9, (
                f"domain {domain_len} / cell {CELL_SIZE_M} != grid {n}"
            )


class TestTimeConstants:
    def test_time_steps(self) -> None:
        assert TIME_STEPS == 31

    def test_dt_seconds(self) -> None:
        assert abs(DT_SECONDS - 10.0) < 1e-12

    def test_t_end_seconds(self) -> None:
        assert abs(T_END_SECONDS - 300.0) < 1e-12

    def test_time_consistency(self) -> None:
        """TIME_STEPS must equal T_END_SECONDS / DT_SECONDS + 1."""
        expected = int(T_END_SECONDS / DT_SECONDS) + 1
        assert TIME_STEPS == expected

    def test_frames_span_full_duration(self) -> None:
        last_frame_time = (TIME_STEPS - 1) * DT_SECONDS
        assert abs(last_frame_time - T_END_SECONDS) < 1e-9


class TestChannels:
    def test_input_channels(self) -> None:
        assert N_INPUT_CHANNELS == 5

    def test_output_channels(self) -> None:
        assert N_OUTPUT_CHANNELS == 3


class TestScenarioSplit:
    def test_total(self) -> None:
        assert N_SCENARIOS_TOTAL == 30

    def test_splits_sum_to_total(self) -> None:
        assert N_SCENARIOS_TRAIN + N_SCENARIOS_VAL + N_SCENARIOS_OOD == N_SCENARIOS_TOTAL

    def test_train_largest(self) -> None:
        assert N_SCENARIOS_TRAIN > N_SCENARIOS_VAL
        assert N_SCENARIOS_TRAIN > N_SCENARIOS_OOD


class TestPhysicalReferences:
    def test_ambient_temperature(self) -> None:
        assert abs(T_AMBIENT_C - 20.0) < 1e-12

    def test_max_temperature(self) -> None:
        assert abs(T_MAX_C - 1200.0) < 1e-12

    def test_v_max(self) -> None:
        assert abs(V_MAX_M - 30.0) < 1e-12

    def test_co_max(self) -> None:
        assert abs(CO_MAX_PPM - 5000.0) < 1e-12


class TestTenability:
    def test_temperature_ordering(self) -> None:
        assert TENABILITY.T_SAFE_C < TENABILITY.T_DANGER_C

    def test_visibility_ordering(self) -> None:
        """Higher visibility is safer — safe_m > danger_m."""
        assert TENABILITY.V_SAFE_M > TENABILITY.V_DANGER_M

    def test_co_ordering(self) -> None:
        assert TENABILITY.CO_SAFE_PPM < TENABILITY.CO_DANGER_PPM

    def test_fed_threshold_in_range(self) -> None:
        assert 0.0 < TENABILITY.FED_THRESHOLD < 1.0

    def test_tenability_values(self) -> None:
        assert abs(TENABILITY.T_SAFE_C - 30.0) < 1e-9
        assert abs(TENABILITY.T_DANGER_C - 60.0) < 1e-9
        assert abs(TENABILITY.V_SAFE_M - 10.0) < 1e-9
        assert abs(TENABILITY.V_DANGER_M - 3.0) < 1e-9
        assert abs(TENABILITY.CO_SAFE_PPM - 100.0) < 1e-9
        assert abs(TENABILITY.CO_DANGER_PPM - 1400.0) < 1e-9
        assert abs(TENABILITY.FED_THRESHOLD - 0.3) < 1e-9

    def test_tenability_is_immutable(self) -> None:
        with pytest.raises((AttributeError, TypeError)):
            TENABILITY.T_SAFE_C = 999.0  # type: ignore[misc]
