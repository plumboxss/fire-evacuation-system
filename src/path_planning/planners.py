"""
Path planning algorithms: weighted A* and fallback BFS.

Implements Week 12. See docs/manual_v2.md.

Finds the safest evacuation path from an occupant position to the
nearest exit on the weighted building graph.
"""
from __future__ import annotations

from typing import List, Optional, Tuple

import numpy as np

from src.risk_map.risk_map_class import RiskMap


class EvacuationPlanner:
    """Weighted A* planner on the building graph.

    Args:
        graph: NetworkX Graph from :func:`~src.path_planning.building_graph.build_graph`.
        heuristic: Distance heuristic: ``"euclidean"`` or ``"manhattan"``.
        max_path_length: Give up if the shortest path exceeds this many nodes.
        fallback_to_last: If re-planning fails, return the last valid path.
    """

    def __init__(
        self,
        graph,
        heuristic: str = "euclidean",
        max_path_length: int = 500,
        fallback_to_last: bool = True,
    ) -> None:
        raise NotImplementedError("Week 12: initialise EvacuationPlanner")

    def plan(
        self,
        start_xyz: np.ndarray,
        risk_map: RiskMap,
        t: float,
    ) -> List[np.ndarray]:
        """Compute the safest path from ``start_xyz`` to the nearest exit.

        Updates edge weights via :func:`~src.path_planning.edge_weights.compute_edge_weights`,
        then runs NetworkX A* to the nearest reachable exit node.

        Args:
            start_xyz: Occupant world position ``[x_m, y_m, z_m]``.
            risk_map: Current risk map for edge weight computation.
            t: Current simulation time in seconds.

        Returns:
            Ordered list of world-space waypoints ``[np.ndarray([x, y, z]), ...]``
            from start to exit (inclusive).
            Returns empty list if no path exists and no fallback is available.

        Raises:
            ValueError: If ``start_xyz`` is out of bounds.
        """
        raise NotImplementedError("Week 12: run weighted A* on building graph")

    def replan(
        self,
        current_xyz: np.ndarray,
        risk_map: RiskMap,
        t: float,
    ) -> List[np.ndarray]:
        """Re-plan from the current position with updated risk information.

        Args:
            current_xyz: Current occupant position in metres.
            risk_map: Updated risk map (e.g., new model prediction).
            t: Current simulation time in seconds.

        Returns:
            New path as in :meth:`plan`.
        """
        raise NotImplementedError("Week 12: re-plan from current position")


if __name__ == "__main__":
    print("planners.py — skeleton only (not yet implemented)")
    print("SKIP")
