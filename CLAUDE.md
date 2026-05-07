# Fire Evacuation Prediction System — Project Context

> **Read this file first.** It is the single source of truth for project constraints,
> conventions, and scope. Never violate the hard constraints below.
>
> When you need detail, refer to:
> - `docs/interface_contracts.md` — exact function signatures
> - `docs/coordinate_convention.md` — coordinate system rules
> - `docs/risk_indicators.md` — tenability thresholds + ISO/SFPE citations
> - `docs/manual_v2.md` — 14-week schedule and rationale
> - `docs/decisions.md` — log of past decisions and their reasons
> - `docs/lessons_learned.md` — mistakes already made; do not repeat

Read these explicitly when relevant. Do **not** auto-load them every session.

---

## What This Project Is

14-week undergraduate engineering capstone competition entry: an
**active fire-response system**.

- **ConvLSTM** and **PI-FNO** models trained on FDS simulation data predict fire spread.
- Predictions are converted to **ISO-13571-based risk maps** (FED + tenability).
- **Weighted A\*** computes dynamic evacuation paths.
- **PyBullet** is used in Week 12 for an integrated single-drone demo.

Three primary research goals:
1. **Speed**: PI-FNO inference 1000× faster than FDS
2. **Generalization**: PI-FNO performs on unseen fire locations / HRR
3. **Path safety**: Dynamic paths reduce cumulative FED vs static paths

---

## Hard Constraints — NEVER Violate

### Geometry

| Parameter | Value |
|-----------|-------|
| Building | Single floor, complex maze layout (multiple rooms, intersections, central courtyard) |
| **FDS MESH** (computational domain) | **100 × 80 × 8 cells** over **[−10, 40] × [−10, 30] × [0, 4] m** |
| **SLCF region** (learnable, model-visible) | **60 × 40 × 6 cells** over **[0, 30] × [0, 20] × [0, 3] m** |
| Cell resolution | **0.5 m × 0.5 m × 0.5 m** |
| External buffer | 10 m on −X, +X, −Y, +Y for ventilation boundaries |

**Critical distinction:** The MESH is what FDS simulates (with buffer). The SLCF
is what models ingest. The buffer exists purely for boundary conditions and is
discarded during data extraction.

### Time

| Parameter | Value |
|-----------|-------|
| Simulation duration | 0–300 s |
| Time steps | **31 frames** at **10 s** intervals |
| FDS `DT_SLCF` | 10.0 |
| Model prediction step | 10 s (single autoregressive step) |
| Predictive horizon | 60 s (6 autoregressive steps) |

### Data

| Parameter | Value |
|-----------|-------|
| Total scenarios | **30** |
| Train / Val / OOD split | 24 / 3 / 3 |
| Fire HRR variations | 500, 1000, 1500, 2000 kW |
| Fire location variations | 6 distinct locations across the maze |
| Ventilation | All scenarios: both end doors open (fixed) |

### Compute

| Parameter | Value |
|-----------|-------|
| Training GPU | NVIDIA A100 40 GB on RunPod |
| Coordinate system | Metres, Z-up, world origin at corner (0, 0, 0) |
| Units | **SI only** — m, s, °C, ppm. NEVER mm. |

---

## Tech Stack

| Layer | Library / Tool |
|-------|---------------|
| Deep learning | Python 3.10+, PyTorch 2.0+, CUDA 11.8+ |
| Neural operator | `neuraloperator` (FNO) |
| FDS data | `fdsreader` |
| Graph / routing | `NetworkX` |
| Interpolation | `scipy.interpolate.RegularGridInterpolator` |
| Drone sim (Wk 12) | `pybullet`, `gym-pybullet-drones` |
| Experiment tracking | Weights & Biases |
| Testing | `pytest` |

---

## Tensor Conventions — CRITICAL

All model code must use these shapes:

```
Model input  : (B, 5, 60, 40, 6)   channels → [T, V, CO, mask, time_enc]
Model output : (B, 3, 60, 40, 6)   channels → [T, V, CO]
```

- All channels normalized to **[0, 1]**
- Convention: **higher value = more dangerous** (channels 0–2)
- Visibility is **INVERSE-mapped**: low visibility → high value
- Time encoding broadcast spatially (constant across grid for each frame)

Single-timestep usage: input is one frame, output is one frame at t+10s.
For 60s horizon, autoregress 6 times (chain output → input).

See `docs/interface_contracts.md` for exact normalisation formulas.

---

## RiskMap Interface (CRITICAL)

```python
from abc import ABC, abstractmethod
import numpy as np

class RiskMap(ABC):
    """Abstract risk map. Three concrete implementations live in src/risk_map/."""

    @abstractmethod
    def query(
        self,
        xyz: np.ndarray,           # shape (3,) or (N, 3) in world metres
        t: float | None = None,    # simulation time in seconds
    ) -> float | np.ndarray:
        """Returns danger ∈ [0, 1].
        Out-of-bounds → 1.0  (safety default)
        Out-of-time-range → 1.0
        """
```

Three concrete implementations:

| Class | Used by | Purpose |
|-------|---------|---------|
| `FDSRiskMap` | data_pipeline, validation | Ground truth from FDS data |
| `FNORiskMap` | evaluation | PI-FNO inference results |
| `DynamicRiskMap` | PyBullet demo (Week 12) | Time-evolving live map |

All three share the same `query()` interface. PyBullet code never knows
which is in use — same call signature.

---

## Tenability Thresholds (ISO 13571 + SFPE Handbook)

| Indicator | Safe | Danger |
|-----------|------|--------|
| Temperature | 30 °C | 60 °C (humid air) |
| Visibility | 10 m | 3 m |
| CO instantaneous | 100 ppm | 1400 ppm |
| FED (CO cumulative) | — | 0.3 (sensitive population) |

Sources: ISO 13571:2012 §5–7; SFPE Handbook 5th Ed. Ch. 63 (Purser & McAllister 2016).
See `docs/risk_indicators.md` for derivation and Korean-language glossary.

---

## What This Project Does NOT Do

Do **not** add these features, even if they seem natural extensions.
Each was explicitly excluded for scope or feasibility reasons (see
`docs/decisions.md` for rationales):

- Multi-floor buildings (single floor only)
- Real-time CFD (FDS pre-computed only)
- Mesh resolution other than 0.5 m
- Drone swarms (single Crazyflie sim)
- Real fire experiments (simulation only)
- Ventilation variation (all scenarios: both doors open)
- HCN, irritant gas, or radiant heat FED (CO only)
- Real human behaviour modelling (idealised evacuees)
- Replacing existing fire safety systems (we are auxiliary)

---

## FDS Input File Conventions — LESSONS LEARNED

These rules have been validated by trial and error. Violating them breaks
the data pipeline:

1. **NEVER set `VECTOR=.TRUE.` on `&SLCF`.**
   Combination of `VECTOR=.TRUE.` and `CELL_CENTERED=.TRUE.` causes
   `fdsreader` to fail with broadcast errors during slice loading.
   Use scalar slices only (3 slices: T, V, CO).

2. **Always use `CELL_CENTERED=.TRUE.`** for SLCF data we feed into models.

3. **`DT_SLCF=10.0`** to align with model time step.

4. **SLCF `XB` must extract** the learnable region [0, 30] × [0, 20] × [0, 3]
   even when the MESH is larger. The MESH may extend beyond for
   ventilation boundaries; the SLCF clips to the actual building footprint.

5. Three SLCF only: `TEMPERATURE`, `SOOT VISIBILITY` (or `VISIBILITY`),
   `VOLUME FRACTION` (with `SPEC_ID='CARBON MONOXIDE'`).

Example correct SLCF:
```
&SLCF QUANTITY='TEMPERATURE',
      CELL_CENTERED=.TRUE.,
      ID='Temperature',
      XB=0.0,30.0, 0.0,20.0, 0.0,3.0/
```

Wrong (causes fdsreader failure):
```
&SLCF QUANTITY='TEMPERATURE',
      VECTOR=.TRUE.,            ← REMOVE THIS LINE
      CELL_CENTERED=.TRUE.,
      ID='Temperature', XB=...
```

---

## Coding Conventions

### Required for all public code

- **Type hints** on every function signature
- **Docstrings** on every public function (Google or NumPy style)
- **Tensor shapes documented** in docstrings: `Args: x: shape (B, 5, 60, 40, 6)`
- **`pathlib.Path`** for file paths, never `os.path.join`
- **`raise ValueError("clear message")`** — never silent failures
- **`if __name__ == '__main__'`** self-test block in computational modules,
  printing PASS/FAIL clearly
- **Absolute imports**: `from src.shared.constants import GRID_SHAPE`
- **YAML** for config files (loaded via `dataclass` or Pydantic)
- **Korean comments OK**, but identifiers must be English

### Forbidden

- Black/Ruff configuration (skip — keep tooling minimal)
- `from foo import *` (always explicit)
- Configuration as raw dicts in production code (use dataclasses)
- Silent exception handling
- Hard-coded numerical constants (use `src/shared/constants.py`)

### Module structure

Every computational module must have:

1. Module docstring (purpose, author, related week in manual)
2. Imports
3. Type-hinted functions/classes with docstrings
4. `if __name__ == '__main__'` self-test that prints `PASS` or `FAIL`

---

## 14-Week Schedule Reference

| Week | Module | Status |
|------|--------|--------|
| 1–2  | Environment setup, building modeling (PyroSim) | — |
| 3–5  | FDS scenario generation (30 runs) | In progress |
| 6    | Data pipeline: extraction, normalisation, masks | — |
| 7    | ConvLSTM baseline | — |
| 8    | PI-FNO no-PI version | — |
| 9    | PI-FNO full (with physics-informed loss) | — |
| 10   | EXP-FIRE-001 evaluation + risk map module | — |
| 11   | Path planning + ablations | — |
| 12   | EXP-PATH-001 + PyBullet integration demo | — |
| 13   | Visualisation, slides | — |
| 14   | Paper draft, code cleanup | — |

See `docs/manual_v2.md` for week-by-week detail.

---

## Workflow Rules

### Module development cycle

1. **Implement** with type hints and docstrings
2. **Self-test** via `__main__` block: `python -m src.module.path`
3. **Human review**: file diff and explanation
4. **Unit test** in `tests/` using pytest
5. **Commit** with clear message

### Decision-making

- **When in doubt about scope, ASK** before expanding
- **Single-purpose functions** — no "while we're at it" features
- **Reference checks before improvement**: confirm interface change is
  necessary before modifying contracts
- **Log major decisions** to `docs/decisions.md` after agreement

### Communicating with this project

- Read `CLAUDE.md` first (you are doing this now)
- Read explicitly referenced docs as needed
- Never auto-load all docs — preserve context budget
- Follow the 8-section task request template (see `docs/task_request_template.md`)

---

## Where Things Go

```
src/shared/        — coordinates, constants, building, normalisation
src/data_pipeline/ — FDS .smv/.sf → .npz conversion
src/dataset/       — PyTorch Dataset and DataLoaders
src/models/        — ConvLSTM, PI-FNO, base classes, losses
src/training/      — training loops, callbacks
src/evaluation/    — metrics, model comparison (EXP-FIRE-001)
src/risk_map/      — risk map conversion, ASET, FED, predictive
src/path_planning/ — graph, A*, evacuation simulator
src/integration/   — PyBullet demo (Week 12)
src/visualization/ — plots, animations
configs/           — YAML hyperparameters per module
experiments/       — executable scripts (exp_*, ablation_*)
notebooks/         — exploratory analysis only (not production code)
tests/             — pytest unit tests mirroring src/ structure
docs/              — project documentation (this is the heart)
checkpoints/       — trained models (.gitignore)
results/           — experiment outputs (CSV, JSON)
figures/           — paper/slide figures
```

---

## Key File Locations

| What | Where |
|------|-------|
| All numerical constants | `src/shared/constants.py` |
| Normalization functions | `src/shared/normalization.py` |
| Coordinate utilities | `src/shared/coordinates.py` |
| Building geometry | `src/shared/building.py` |
| RiskMap abstract base | `src/risk_map/risk_map_class.py` |
| Interface contracts | `docs/interface_contracts.md` |
| Coordinate conventions | `docs/coordinate_convention.md` |
| Tenability reference | `docs/risk_indicators.md` |
| 14-week manual | `docs/manual_v2.md` |
| Decision log | `docs/decisions.md` |
| Lessons learned | `docs/lessons_learned.md` |
| Task request template | `docs/task_request_template.md` |
