"""
Tests for src/shared/normalization.py — Tier 1 (must pass from day 1).

Tests round-trip identity, boundary clipping, monotonicity,
and the inverse-mapping property of visibility.
"""
import numpy as np
import pytest

from src.shared.normalization import (
    denormalize_co,
    denormalize_temperature,
    denormalize_visibility,
    normalize_co,
    normalize_temperature,
    normalize_visibility,
)

TOL = 1e-9  # Round-trip absolute tolerance


class TestTemperature:
    def test_normalize_ambient_is_zero(self) -> None:
        assert abs(float(normalize_temperature(np.array([20.0]))[0])) < TOL

    def test_normalize_max_is_one(self) -> None:
        assert abs(float(normalize_temperature(np.array([1200.0]))[0]) - 1.0) < TOL

    def test_clips_below_ambient(self) -> None:
        val = float(normalize_temperature(np.array([0.0]))[0])
        assert val == 0.0, f"Expected 0.0, got {val}"

    def test_clips_above_max(self) -> None:
        val = float(normalize_temperature(np.array([9999.0]))[0])
        assert val == 1.0, f"Expected 1.0, got {val}"

    def test_round_trip(self) -> None:
        vals = np.array([20.0, 100.0, 300.0, 600.0, 1200.0])
        recovered = denormalize_temperature(normalize_temperature(vals))
        np.testing.assert_allclose(recovered, vals, atol=TOL)

    def test_monotonically_increasing(self) -> None:
        vals = np.linspace(20.0, 1200.0, 50)
        normed = normalize_temperature(vals)
        assert (np.diff(normed) >= 0).all()

    def test_output_shape_preserved(self) -> None:
        arr = np.ones((3, 4, 5)) * 500.0
        assert normalize_temperature(arr).shape == (3, 4, 5)

    def test_output_dtype_is_float64(self) -> None:
        arr = np.array([100.0], dtype=np.float32)
        assert normalize_temperature(arr).dtype == np.float64


class TestVisibility:
    def test_normalize_max_vis_is_zero(self) -> None:
        """30 m visibility → 0.0 (safe = low danger)."""
        val = float(normalize_visibility(np.array([30.0]))[0])
        assert abs(val) < TOL

    def test_normalize_zero_vis_is_one(self) -> None:
        """0 m visibility → 1.0 (dangerous = high danger)."""
        val = float(normalize_visibility(np.array([0.0]))[0])
        assert abs(val - 1.0) < TOL

    def test_clips_above_max(self) -> None:
        val = float(normalize_visibility(np.array([100.0]))[0])
        assert val == 0.0

    def test_negative_treated_as_zero(self) -> None:
        val = float(normalize_visibility(np.array([-5.0]))[0])
        assert val == 1.0

    def test_inverse_monotonicity(self) -> None:
        """Higher visibility should give strictly lower normalised value."""
        vals = np.array([0.0, 3.0, 5.0, 10.0, 20.0, 30.0])
        normed = normalize_visibility(vals)
        assert (np.diff(normed) <= 0).all()

    def test_round_trip(self) -> None:
        vals = np.array([0.0, 3.0, 10.0, 15.0, 30.0])
        recovered = denormalize_visibility(normalize_visibility(vals))
        np.testing.assert_allclose(recovered, vals, atol=TOL)

    def test_output_shape_preserved(self) -> None:
        arr = np.ones((2, 6)) * 10.0
        assert normalize_visibility(arr).shape == (2, 6)


class TestCO:
    def test_normalize_zero_is_zero(self) -> None:
        val = float(normalize_co(np.array([0.0]))[0])
        assert abs(val) < TOL

    def test_normalize_max_is_one(self) -> None:
        val = float(normalize_co(np.array([5000.0]))[0])
        assert abs(val - 1.0) < TOL

    def test_clips_below_zero(self) -> None:
        val = float(normalize_co(np.array([-100.0]))[0])
        assert val == 0.0

    def test_clips_above_max(self) -> None:
        val = float(normalize_co(np.array([1e7]))[0])
        assert val == 1.0

    def test_round_trip(self) -> None:
        vals = np.array([0.0, 100.0, 500.0, 1400.0, 5000.0])
        recovered = denormalize_co(normalize_co(vals))
        np.testing.assert_allclose(recovered, vals, atol=TOL)

    def test_monotonically_increasing(self) -> None:
        vals = np.linspace(0.0, 5000.0, 100)
        normed = normalize_co(vals)
        assert (np.diff(normed) >= 0).all()

    def test_log_scale_compresses_high_values(self) -> None:
        """100→200 ppm gap should map to larger normalised delta than 4900→5000."""
        d_low = float(normalize_co(np.array([200.0]))[0]) - float(
            normalize_co(np.array([100.0]))[0]
        )
        d_high = float(normalize_co(np.array([5000.0]))[0]) - float(
            normalize_co(np.array([4900.0]))[0]
        )
        assert d_low > d_high, "Log scale should compress high-ppm range"

    def test_output_shape_preserved(self) -> None:
        arr = np.ones((60, 40, 6)) * 300.0
        assert normalize_co(arr).shape == (60, 40, 6)


class TestCrossChannelConsistency:
    """Sanity checks across all three channels."""

    def test_all_channels_in_unit_interval(self) -> None:
        rng = np.random.default_rng(0)
        T = rng.uniform(20, 1200, 1000)
        V = rng.uniform(0, 30, 1000)
        CO = rng.uniform(0, 5000, 1000)

        for arr, fn, name in [
            (T, normalize_temperature, "T"),
            (V, normalize_visibility, "V"),
            (CO, normalize_co, "CO"),
        ]:
            normed = fn(arr)
            assert normed.min() >= 0.0, f"{name}: min < 0"
            assert normed.max() <= 1.0, f"{name}: max > 1"
