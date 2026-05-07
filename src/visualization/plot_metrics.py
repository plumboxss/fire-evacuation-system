"""
Visualise training curves and evaluation metric comparisons.

Implements Week 14. See docs/manual_v2.md.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional


def plot_training_curves(
    train_losses: List[float],
    val_losses: List[float],
    model_name: str = "model",
    output_path: Optional[Path] = None,
) -> None:
    """Plot training and validation loss curves.

    Args:
        train_losses: Per-epoch training losses.
        val_losses: Per-epoch validation losses.
        model_name: Label for the figure title.
        output_path: Optional save path.
    """
    raise NotImplementedError("Week 14: plot loss curves with matplotlib")


def plot_metric_comparison(
    metrics: Dict[str, Dict[str, float]],
    output_path: Optional[Path] = None,
) -> None:
    """Bar chart comparing metrics across models.

    Args:
        metrics: ``{model_name: {metric_name: value}}``.
        output_path: Optional save path.
    """
    raise NotImplementedError("Week 14: plot grouped bar chart of model metrics")


if __name__ == "__main__":
    print("plot_metrics.py — skeleton only (not yet implemented)")
    print("SKIP")
