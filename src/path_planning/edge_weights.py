"""
Edge weight computation for the building graph.

Implements Week 12. See docs/manual_v2.md.

Edge cost = base_cost + risk_scale × danger(v)
Edges where danger(v) > risk_threshold are removed (impassable).

Config: configs/path_planning.yaml → edge_weights
"""
from __future__ import annotations

import numpy as np

from src.risk_map.risk_map_class import RiskMap


def compute_edge_weights(
    graph,
    risk_map: RiskMap,
    t: float,
    base_cost: float = 1.0,
    risk_scale: float = 10.0,
    risk_threshold: float = 0.9,
) -> None:
    """Update edge weights in-place based on the current risk map.

    Iterates over all edges ``(u, v)`` and sets
    ``graph[u][v]["weight"] = base_cost + risk_scale * risk_map.query(v_xyz, t)``.
    Edges where ``risk_map.query(v_xyz, t) > risk_threshold`` are marked
    ``"passable": False``.

    Args:
        graph: NetworkX Graph from :func:`building_graph.build_graph`.
        risk_map: A :class:`~src.risk_map.risk_map_class.RiskMap` instance.
        t: Current simulation time in seconds.
        base_cost: Cost per unit step in the absence of danger.
        risk_scale: Multiplier applied to the danger value.
        risk_threshold: Cells above this danger level are marked impassable.

    Raises:
        ValueError: If ``graph`` nodes are missing ``"world_xyz"`` attribute.
    """
    raise NotImplementedError("Week 12: update edge weights from risk map query")


def remove_impassable_edges(graph) -> int:
    """Remove all edges marked ``passable=False`` from the graph.

    Args:
        graph: NetworkX Graph (modified in-place).

    Returns:
        Number of edges removed.
    """
    raise NotImplementedError("Week 12: filter impassable edges from graph")


if __name__ == "__main__":
    print("edge_weights.py — skeleton only (not yet implemented)")
    print("SKIP")
