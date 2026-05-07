"""
Step-by-step evacuation simulation with dynamic re-planning.

Implements Week 12. See docs/manual_v2.md.

Simulates an occupant following the planned path, accumulating FED,
and re-planning every 10 seconds as new fire predictions become available.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import numpy as np


@dataclass
class EvacuationResult:
    """Outcome of a single evacuation simulation run."""

    success: bool
    """True if occupant reached an exit before incapacitation."""

    trajectory: List[np.ndarray] = field(default_factory=list)
    """World-space waypoints visited, each ``[x, y, z]`` in metres."""

    times: List[float] = field(default_factory=list)
    """Simulation times corresponding to each waypoint, in seconds."""

    fed_history: List[float] = field(default_factory=list)
    """Accumulated FED at each time step."""

    exit_time: float = float("inf")
    """Time the occupant reached the exit (seconds). inf if not reached."""


def simulate_evacuation(
    start_xyz: np.ndarray,
    model_output_sequence: np.ndarray,
    obstacle_mask: np.ndarray,
    exits: List,
    replan_interval: float = 10.0,
) -> EvacuationResult:
    """Simulate one occupant evacuating from ``start_xyz``.

    At each replan step, builds a fresh risk map from the model prediction
    and calls :meth:`~src.path_planning.planners.EvacuationPlanner.replan`.
    FED is accumulated along the trajectory.

    Args:
        start_xyz: Initial occupant position ``[x_m, y_m, z_m]``.
        model_output_sequence: ``(T, 3, 60, 40, 6)`` model predictions.
        obstacle_mask: ``(60, 40, 6)`` fluid/solid mask.
        exits: List of exit world coordinates in metres.
        replan_interval: Re-planning cadence in seconds. Default 10 s.

    Returns:
        :class:`EvacuationResult` with full trajectory and outcome.

    Raises:
        ValueError: If ``start_xyz`` is out of domain bounds.
    """
    raise NotImplementedError("Week 12: implement step-by-step evacuation simulation")


if __name__ == "__main__":
    print("evacuation_sim.py — skeleton only (not yet implemented)")
    print("SKIP")
