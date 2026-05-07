"""
Tests for src/risk_map/.

Implements Week 12 tests. See docs/manual_v2.md.
Fill in test bodies once the risk map module is implemented.
"""
from __future__ import annotations

import pytest
import numpy as np

from src.shared.constants import GRID_SHAPE


class TestStaticRiskMap:
    def test_query_in_bounds_returns_float(self) -> None:
        """query() on a valid coordinate should return a float in [0, 1]."""
        raise NotImplementedError("Week 12: test after StaticRiskMap is implemented")

    def test_query_out_of_bounds_returns_one(self) -> None:
        """query() outside the building domain must return 1.0."""
        raise NotImplementedError("Week 12: verify out-of-bounds safety default")

    def test_query_safe_cell_low_danger(self) -> None:
        """A cell with zero normalised fields should have danger near 0."""
        raise NotImplementedError("Week 12: check danger for all-zero field")

    def test_query_dangerous_cell_high_danger(self) -> None:
        """A cell with all fields at 1.0 should have danger near 1.0."""
        raise NotImplementedError("Week 12: check danger for all-ones field")


class TestTenability:
    def test_temperature_danger_safe(self) -> None:
        """Normalised T below safe threshold maps to danger ≈ 0."""
        raise NotImplementedError("Week 12: test temperature_danger at safe level")

    def test_visibility_danger_inverse(self) -> None:
        """High V_norm (low visibility) should produce high danger."""
        raise NotImplementedError("Week 12: test visibility_danger direction")

    def test_aggregate_weights_sum(self) -> None:
        """Weights 0.4 + 0.4 + 0.2 should sum to 1.0."""
        raise NotImplementedError("Week 12: verify weight sum constraint")


class TestFED:
    def test_zero_co_gives_zero_fed(self) -> None:
        """Zero CO over any duration should yield FED = 0."""
        raise NotImplementedError("Week 12: test FED with zero CO")

    def test_fed_increases_monotonically(self) -> None:
        """FED accumulated over longer exposures should be >= shorter ones."""
        raise NotImplementedError("Week 12: test FED monotonicity over time")
