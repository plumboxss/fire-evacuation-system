"""
Build a NetworkX graph from the building grid for path planning.

Implements Week 12. See docs/manual_v2.md.

Creates a 6-connected graph (±x, ±y, ±z faces) over the 60×40×6 grid.
Solid cells are excluded; exits are added as terminal nodes.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

import numpy as np

try:
    import networkx as nx
except ImportError:
    nx = None  # type: ignore[assignment]


def build_graph(
    obstacle_mask: np.ndarray,
    exits: List[Tuple[float, float, float]],
) -> "nx.Graph":
    """Build a 6-connected grid graph for the single-floor building.

    Args:
        obstacle_mask: Boolean array ``(60, 40, 6)``.
                       True = solid (cell excluded from graph).
        exits: List of exit world coordinates ``[(x, y, z), ...]`` in metres.

    Returns:
        NetworkX undirected Graph.
        Node IDs: tuples ``(ix, iy, iz)``.
        Each node carries attribute ``"world_xyz": np.ndarray`` (metres).
        Exit nodes additionally carry ``"is_exit": True``.

    Raises:
        ImportError: If ``networkx`` is not installed.
        ValueError: If ``obstacle_mask.shape != (60, 40, 6)``.
    """
    raise NotImplementedError("Week 12: build 6-connected graph over fluid cells")


def add_exit_nodes(
    graph: "nx.Graph",
    exits: List[Tuple[float, float, float]],
) -> "nx.Graph":
    """Mark exit nodes in the graph and connect them to adjacent grid cells.

    Args:
        graph: Building graph from :func:`build_graph`.
        exits: Exit world coordinates in metres.

    Returns:
        Modified graph with exit nodes tagged ``is_exit=True``.
    """
    raise NotImplementedError("Week 12: find nearest grid nodes to each exit coordinate")


if __name__ == "__main__":
    print("building_graph.py — skeleton only (not yet implemented)")
    print("SKIP")
