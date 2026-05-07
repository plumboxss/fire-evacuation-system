# Project Manual v2 — 14-Week Implementation Schedule

> Detailed week-by-week implementation guide for the fire evacuation
> prediction system. This document complements `CLAUDE.md` (project
> context) and provides the **execution plan**.

---

## Overview

| Phase | Weeks | Focus |
|-------|-------|-------|
| **A. Foundation** | 1–5 | Environment, geometry, FDS data generation |
| **B. Pipeline** | 6 | FDS → .npz conversion |
| **C. ConvLSTM** | 7 | Baseline model |
| **D. PI-FNO** | 8–9 | Neural operator + physics loss |
| **E. Risk + Path** | 10–11 | Risk maps and path planning |
| **F. Integration** | 12 | PyBullet demo + EXP-PATH-001 |
| **G. Reporting** | 13–14 | Visualisation, paper, slides |

---

## Phase A: Foundation (Weeks 1–5)

### Week 1: Environment Setup

- Set up Python venv, RunPod GPU instance, W&B project
- Clone repo, create skeleton (see Claude Code prompt for skeleton creation)
- Verify FDS + Smokeview installation locally
- PyroSim license verified

### Week 2: Coordinate System Document

- Lock down `docs/coordinate_convention.md` definitions
- Implement `src/shared/coordinates.py` with full unit tests
- Implement `src/shared/constants.py`
- Verify FDS `&MESH` and SLCF `XB` produce expected (60, 40, 6) shape
- Test fdsreader on a single dummy FDS scenario

### Week 3: Building Geometry

- Build the maze-style single-floor layout in PyroSim
  - Multiple rooms, intersections, central courtyard
  - Two end exits, internal door connections
  - Designed for non-trivial path planning (Dijkstra ≠ optimal)
- Export `.fds` template
- **Critical**: SLCF lines must be:
  ```
  &SLCF QUANTITY='TEMPERATURE',
        CELL_CENTERED=.TRUE.,
        ID='Temperature',
        XB=0.0,30.0, 0.0,20.0, 0.0,3.0/
  ```
  **No `VECTOR=.TRUE.`** (causes fdsreader bug — see `lessons_learned.md`)

### Weeks 4–5: FDS Scenario Generation

- 30 scenarios: 4 HRR levels × 6 fire locations + small variation
- HRR: 500, 1000, 1500, 2000 kW
- Fire locations: 6 distinct cells across the maze
- Ventilation: both end doors open (fixed)
- Run on RunPod CPU instances or local cluster (FDS is CPU-bound)
- Estimate: ~30 CPU-hours total per scenario at this resolution
- Save organized as `data/raw/scenario_NNN/` directories

**Validation per scenario** (do NOT skip):
- `.smv` file exists
- 3 `.sf` files: temperature, visibility, CO
- `fdsreader` loads cleanly: `to_global(return_coordinates=True)` succeeds
- Output shape is `(31, 60, 40, 6)`

---

## Phase B: Pipeline (Week 6)

Goal: convert raw FDS output → trainable `.npz` files.

### Modules to implement

1. `src/data_pipeline/fds_extractor.py`
   - Function: `extract_slices(fds_dir: Path) -> dict`
   - Returns un-normalised `(31, 60, 40, 6)` arrays for T, V, CO + coords + times
   - Self-test on one scenario; verify shapes match interface contract

2. `src/data_pipeline/normalize.py`
   - Apply normalisation rules from `interface_contracts.md`
   - Bidirectional: `normalize_X` and `denormalize_X` for unit tests

3. `src/data_pipeline/mask_generator.py`
   - Generate `(60, 40, 6)` building mask from PyroSim geometry
   - Save once to `data/building_mask.npz`
   - All scenarios share this mask (geometry constant)

4. `src/dataset/fire_dataset.py`
   - PyTorch `Dataset` with `(t, t+1)` pairs
   - Returns `(x: (5, 60, 40, 6), y: (3, 60, 40, 6))`
   - Splits: train (24 scenarios), val (3), test_ood (3)

5. `src/data_pipeline/build_dataset.py`
   - Top-level script: process all 30 scenarios → `dataset.h5`
   - Logs scenario metadata into HDF5 attrs

### Validation

- 720 training pairs (24 × 30) accessible via DataLoader
- Random pair has correct shape and value range [0, 1]
- Mask correctly matches building geometry visually
- Time encoding has expected shape and range

---

## Phase C: ConvLSTM Baseline (Week 7)

Goal: train a working baseline that PI-FNO will be compared against.

### Modules to implement

1. `src/models/conv_lstm_3d.py`
   - 3D ConvLSTM with (B, 5, 60, 40, 6) → (B, 3, 60, 40, 6)
   - Reference: existing 2D ConvLSTM implementation, extended to 3D
   - Self-test: forward pass shape check, backward pass gradient check

2. `src/training/trainer.py`
   - Generic training loop, model-agnostic
   - W&B logging, checkpointing, LR scheduling

3. `src/training/train_conv_lstm.py`
   - Entry point: loads `configs/conv_lstm.yaml`, trains model
   - Saves `checkpoints/conv_lstm_best.pt`

4. Train and record baseline metrics on val set:
   - RMSE per channel
   - SSIM per channel
   - Inference time per frame

---

## Phase D: PI-FNO (Weeks 8–9)

### Week 8: PI-FNO without physics loss

- `src/models/fno.py` — wrap `neuraloperator.FNO` for our shapes
- Same training procedure as ConvLSTM, MSE loss only
- Compare to ConvLSTM: this isolates "what does the FNO architecture buy us?"

### Week 9: Add physics-informed loss

- `src/training/losses.py` — add PDE residual loss
  - Heat diffusion analogue (rough, not exact CFD)
  - Mass-conservation constraint on CO
- Combined loss: `L = L_data + λ · L_phys`
- Train; compare to no-PI version

### Validation: EXP-FIRE-001 (Week 10)

- ConvLSTM vs PI-FNO no-PI vs PI-FNO full
- Same val and OOD splits
- Same metrics (RMSE, SSIM, peak danger error)
- Output: `results/exp_fire_001/comparison.csv` + figure

---

## Phase E: Risk + Path (Weeks 10–11)

### Week 10: Risk Map Module

1. `src/risk_map/tenability.py` — compute `d_T`, `d_V`, `d_CO_inst`
2. `src/risk_map/fed.py` — accumulate path-integrated FED
3. `src/risk_map/risk_map_class.py` — abstract base + 3 concrete classes
4. `src/risk_map/predictive.py` — autoregress PI-FNO 6 steps for 60s horizon

EXP-RISK-001: compare FDS ground truth vs PI-FNO predicted risk maps.

### Week 11: Path Planning

1. `src/path_planning/building_graph.py` — build NetworkX graph from
   maze geometry (16–20 nodes)
2. `src/path_planning/edge_weights.py` — convert risk map → edge weights
3. `src/path_planning/planners.py` — three concrete planners:
   - `DijkstraPlanner` (no risk awareness)
   - `StaticAvoidancePlanner` (current risk only)
   - `DynamicPredictivePlanner` (60s predictive risk, 30s replan period)
4. `src/path_planning/evacuation_sim.py` — simulate occupant moving
   along planned path, record FED accumulation

---

## Phase F: Integration + EXP-PATH-001 (Week 12)

### PyBullet Demo

1. `src/integration/pybullet_demo.py`
   - Load building URDF
   - Spawn single Crazyflie drone
   - At each timestep:
     - Drone position from `getBasePositionAndOrientation`
     - Query `DynamicRiskMap` at drone pos
     - If risk > threshold, replan and steer to next waypoint
2. Visualize risk field as 2D overlay (Z = 1 m slice)

### EXP-PATH-001

Compare three planners on multiple OOD scenarios:

| Planner | Risk awareness | Replan |
|---------|----------------|--------|
| Dijkstra | None | Never |
| Static | Current only | Never |
| Dynamic | 60 s predictive | Every 30 s |

Metrics:
- Cumulative FED of evacuee (lower is better)
- Reach time (s)
- % paths intersecting high-danger cells (d > 0.7)

Output: `results/exp_path_001/comparison.csv` + figure.

---

## Phase G: Reporting (Weeks 13–14)

### Week 13: Visualisation

- `src/visualization/plot_fire_evolution.py` — animate T/V/CO over time
- `src/visualization/plot_risk_map.py` — colour-coded danger overlay
- `src/visualization/plot_paths.py` — overlay 3 planner outputs on map
- Save figures into `figures/` for paper

### Week 14: Paper + Slides

- Final EXP-FIRE-001, EXP-RISK-001, EXP-PATH-001 results
- Code review and cleanup
- Tag a release: `v1.0-final`

---

## Risk Register (Things That Will Likely Go Wrong)

| Risk | Mitigation |
|------|-----------|
| `fdsreader` fails on a scenario | Validate every scenario in Week 4–5 before model training |
| Single FDS scenario takes >12 hours | Reduce SLCF dump frequency; we only need 31 frames |
| ConvLSTM doesn't learn (loss flat) | Verify input is normalised; check mask is bool not float |
| PI-FNO physics loss explodes | Start with `λ = 0.001` and curriculum-increase |
| Path planner suggests through walls | Test graph connectivity carefully; verify A* respects edges |
| PyBullet drone falls through floor | Set drone collision filter; drone is a point mass for our purposes |

---

## Cross-References

- `CLAUDE.md` — project constraints (read first)
- `docs/interface_contracts.md` — exact function signatures
- `docs/coordinate_convention.md` — coordinate system rules
- `docs/risk_indicators.md` — tenability thresholds and FED formula
- `docs/decisions.md` — log of past major decisions
- `docs/lessons_learned.md` — concrete bugs encountered and fixed
