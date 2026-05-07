"""
Physics-informed loss terms for the PI-FNO model.

Implements Week 11. See docs/manual_v2.md.

Provides PDE residual losses (heat diffusion, species transport) and
boundary condition losses that are added to the supervised data loss
during PI-FNO training.

Loss weight configuration: configs/pi_fno.yaml → loss_weights
"""
from __future__ import annotations

from typing import Dict


def heat_diffusion_residual(pred, alpha: float = 1e-4):
    """Compute the heat diffusion PDE residual.

    Residual: ∂T/∂t − α∇²T = 0 (simplified, no source term).

    Args:
        pred: Predicted temperature field ``(B, 60, 40, 6)``, normalised.
        alpha: Thermal diffusivity coefficient.

    Returns:
        Scalar loss (mean squared PDE residual).

    Raises:
        ValueError: If ``pred`` shape is not ``(B, 60, 40, 6)``.
    """
    raise NotImplementedError("Week 11: compute heat diffusion residual via finite differences")


def species_transport_residual(pred_co, pred_v):
    """Compute the species transport PDE residual for CO and visibility.

    Residual: ∂φ/∂t + ∇·(uφ) = 0 (simplified advection–diffusion).

    Args:
        pred_co: Predicted CO field ``(B, 60, 40, 6)``, normalised.
        pred_v:  Predicted visibility field ``(B, 60, 40, 6)``, normalised.

    Returns:
        Scalar loss (mean squared residual averaged over CO and visibility).
    """
    raise NotImplementedError("Week 11: compute species transport residual")


def boundary_condition_loss(pred, mask):
    """Penalise non-zero predicted values at solid (obstacle) cells.

    Solid cells should have zero flux: enforce pred * (1 − mask) ≈ 0.

    Args:
        pred: Predicted field ``(B, C, 60, 40, 6)``.
        mask: Fluid mask ``(B, 1, 60, 40, 6)`` or ``(60, 40, 6)``.
              1.0 = fluid, 0.0 = solid.

    Returns:
        Scalar loss (mean squared prediction at solid cells).
    """
    raise NotImplementedError("Week 11: enforce zero-flux boundary condition on solid cells")


def combined_pi_loss(
    pred,
    target,
    mask,
    weights: Dict[str, float],
) -> Dict[str, object]:
    """Combine data loss and all physics-informed loss terms.

    Args:
        pred: Model output ``(B, 3, 60, 40, 6)``.
        target: Ground-truth ``(B, 3, 60, 40, 6)``.
        mask: Fluid mask ``(60, 40, 6)`` or ``(B, 1, 60, 40, 6)``.
        weights: Dict with keys ``"data"``, ``"pde_heat"``,
                 ``"pde_species"``, ``"boundary"``.

    Returns:
        Dict with keys ``"total"``, ``"data"``, ``"pde_heat"``,
        ``"pde_species"``, ``"boundary"`` — all scalar tensors.
    """
    raise NotImplementedError("Week 11: assemble weighted combined PI loss")


if __name__ == "__main__":
    print("pi_losses.py — skeleton only (not yet implemented)")
    print("SKIP")
