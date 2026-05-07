# Integration Module — Week 12 Demo

> **Scope**: This module is the exclusive responsibility of **Team Member D**.
> Other team members should not modify files here without coordination.

---

## Purpose

Week 12 integration demo: a single PyBullet drone follows an evacuation path
computed by `src/path_planning/` through a simulated building interior.

The demo pipeline is:

1. Load a trained model (ConvLSTM or PI-FNO) from `checkpoints/`.
2. Run inference on a test FDS scenario to produce fire predictions.
3. Convert predictions to a `PredictiveRiskMap` (from `src/risk_map/`).
4. Plan an evacuation path with `EvacuationPlanner` (from `src/path_planning/`).
5. Spawn a PyBullet environment with the building geometry.
6. Command a single drone to follow the computed waypoints.
7. Log the trajectory and FED exposure to W&B.

---

## Dependencies

```python
import pybullet          # Simulation
import gym_pybullet_drones  # Drone dynamics
```

These are **week-12-only** dependencies. Do not import them in any other module.

---

## Files (to be created in Week 12)

| File | Description |
|------|-------------|
| `pybullet_env.py` | PyBullet scene setup: floor, walls, exits |
| `drone_controller.py` | Waypoint-following drone PID controller |
| `demo_runner.py` | End-to-end demo: model → risk map → path → sim |

---

## Notes

- Single drone only (swarms are out of scope).
- The demo uses pre-computed FDS data — no live CFD.
- Coordinate system is identical to the rest of the project (see
  `docs/coordinate_convention.md`).
