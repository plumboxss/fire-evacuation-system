"""
Tests for ConvLSTM3D and PI-FNO models.

Implements Week 9–11 tests. See docs/manual_v2.md.
Fill in test bodies once models are implemented.
"""
from __future__ import annotations

import pytest

from src.shared.constants import GRID_SHAPE, N_INPUT_CHANNELS, N_OUTPUT_CHANNELS


class TestConvLSTM3D:
    def test_output_shape(self) -> None:
        """Forward pass should produce (B, 3, 60, 40, 6)."""
        raise NotImplementedError("Week 9: test after ConvLSTM3D is implemented")

    def test_output_range(self) -> None:
        """Output values should be in [0, 1] after sigmoid/clamp."""
        raise NotImplementedError("Week 9: verify output range")

    def test_parameter_count_reasonable(self) -> None:
        """hidden_dim=32 model should have < 5M parameters."""
        raise NotImplementedError("Week 9: check parameter count")

    def test_gradient_flows(self) -> None:
        """All parameters should have gradients after backward pass."""
        raise NotImplementedError("Week 9: check grad.is_none for all params")


class TestPIFNO:
    def test_output_shape(self) -> None:
        """Forward pass should produce (B, 3, 60, 40, 6)."""
        raise NotImplementedError("Week 11: test after PI-FNO is implemented")

    def test_output_range(self) -> None:
        """Output values should be in [0, 1]."""
        raise NotImplementedError("Week 11: verify output range")

    def test_pi_loss_terms_finite(self) -> None:
        """All PI loss terms should be finite scalars."""
        raise NotImplementedError("Week 11: check loss finiteness")
