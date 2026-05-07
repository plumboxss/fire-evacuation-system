"""
Tests for src/path_planning/.

Implements Week 12 tests. See docs/manual_v2.md.
Fill in test bodies once path planning is implemented.
"""
from __future__ import annotations

import pytest
import numpy as np

from src.shared.constants import GRID_SHAPE


class TestBuildingGraph:
    def test_graph_has_correct_node_count(self) -> None:
        """Open-floor graph (no obstacles) should have 60*40*6 = 14400 nodes."""
        raise NotImplementedError("Week 12: test after build_graph is implemented")

    def test_exit_nodes_marked(self) -> None:
        """Exit nodes should carry is_exit=True attribute."""
        raise NotImplementedError("Week 12: verify exit node attributes")

    def test_solid_cells_excluded(self) -> None:
        """Nodes corresponding to solid cells must not appear in the graph."""
        raise NotImplementedError("Week 12: test obstacle exclusion")


class TestEvacuationPlanner:
    def test_plan_returns_path_to_exit(self) -> None:
        """plan() should return a non-empty list ending at an exit cell."""
        raise NotImplementedError("Week 12: test path terminates at exit")

    def test_plan_avoids_high_risk_cells(self) -> None:
        """Path should route around cells with danger > risk_threshold."""
        raise NotImplementedError("Week 12: test risk-aware routing")

    def test_plan_returns_empty_if_blocked(self) -> None:
        """plan() should return [] if all exits are surrounded by impassable cells."""
        raise NotImplementedError("Week 12: test no-path fallback")

    def test_replan_updates_path(self) -> None:
        """replan() with new risk information should produce a different path."""
        raise NotImplementedError("Week 12: test dynamic re-planning")
