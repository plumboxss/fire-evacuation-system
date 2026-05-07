"""
Ablation: Effect of physics-informed loss weights on PI-FNO accuracy.

Implements Week 11 ablation. See docs/manual_v2.md.

Trains PI-FNO with 4 loss configurations and reports validation RMSE:
    1. data-only (w_pde=0, w_bc=0)
    2. +heat PDE  (w_pde_heat=0.1)
    3. +species   (w_pde_species=0.05)
    4. full PI-FNO (all losses active)

Usage:
    python experiments/ablation_pi_losses.py
"""
from __future__ import annotations

from pathlib import Path


def main(
    dataset_path: Path = Path("data/processed/dataset.h5"),
    output_dir: Path = Path("results/ablation_pi_losses"),
) -> None:
    """Train PI-FNO with each loss configuration and collect results.

    Args:
        dataset_path: Processed HDF5 dataset.
        output_dir: Output directory for per-run checkpoints and metrics.
    """
    raise NotImplementedError("Week 11: run PI loss weight ablation")


if __name__ == "__main__":
    main()
