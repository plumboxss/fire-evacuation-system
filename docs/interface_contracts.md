# Interface Contracts

> Module-level interface specifications for the fire evacuation system.
> Each section defines the **exact** tensors, types, and conventions that
> modules must honour. Changes here require updating all consuming modules.

---

## 1. Model Input / Output

### Input Tensor

```
Shape  : (B, 5, 60, 40, 6)
Dtype  : torch.float32
Range  : [0, 1]   (all channels)
Device : CUDA (training) or CPU (inference)
```

Channel layout (dimension 1):

| Index | Name | Raw unit | Normalisation |
|-------|------|----------|---------------|
| 0 | Temperature | °C | `(T − 20) / 1180`, clipped to [0, 1] |
| 1 | Visibility | m | `1 − clip(V / 30, 0, 1)`  ← **INVERSE** mapping |
| 2 | CO | ppm | `log1p(CO) / log1p(5000)`, clipped to [0, 1] |
| 3 | Mask | — | 1.0 = fluid (free) cell, 0.0 = solid (wall) |
| 4 | Time encoding | — | `sin(2π · t / 300)`, broadcast to grid |

Convention: **higher value = more dangerous** for channels 0–2.

The time encoding uses `sin(2π · t / 300)` (not the raw `t / T_end`)
to provide a smooth periodic-like signal suitable for ConvLSTM/FNO
inductive biases. It is broadcast as a constant value across the
spatial grid for each frame.

### Output Tensor

```
Shape  : (B, 3, 60, 40, 6)
Dtype  : torch.float32
Range  : [0, 1]
```

Channel layout (dimension 1):

| Index | Name | Same normalisation as input |
|-------|------|-----------------------------|
| 0 | Temperature | Yes |
| 1 | Visibility | Yes (inverse) |
| 2 | CO | Yes |

Mask and time encoding are not predicted (mask is constant; time is known).

### Single-step prediction

The model predicts **one step ahead**: input is frame `t`, output is
frame `t + 10s`. For 60 s horizon, autoregress 6 times, feeding the
predicted output back as the next input (with mask kept and time
encoding incremented).

```python
state = initial_state  # shape (5, 60, 40, 6)
predictions = []
for step in range(6):
    next_state = model(state.unsqueeze(0)).squeeze(0)  # (3, 60, 40, 6)
    predictions.append(next_state)
    # Reconstruct full input for next iteration
    new_input = torch.zeros(5, 60, 40, 6)
    new_input[:3] = next_state
    new_input[3]  = state[3]                                # mask unchanged
    new_input[4]  = compute_time_encoding(t + (step + 1) * 10)
    state = new_input
```

---

## 2. RiskMap Contract

```python
from abc import ABC, abstractmethod
import numpy as np

class RiskMap(ABC):
    """Risk map abstract interface.

    Three concrete implementations exist:
    - FDSRiskMap     : ground truth, used for training/validation
    - FNORiskMap     : PI-FNO inference results, used for evaluation
    - DynamicRiskMap : time-evolving live map, used in PyBullet demo
    """

    @abstractmethod
    def query(
        self,
        xyz: np.ndarray,
        t: float | None = None,
    ) -> float | np.ndarray:
        """Return danger level at world coordinate(s) xyz in metres.

        Args:
            xyz: shape (3,) for single point → returns float.
                 shape (N, 3) for batch     → returns (N,) array.
                 Coordinates in world metres (Z-up, origin at (0, 0, 0)).
            t:   Query time in seconds. If None, uses the most recent
                 available frame.

        Returns:
            Danger level ∈ [0, 1].

        Out-of-bounds rules (return 1.0 — max danger):
            - x < 0 or x > 30
            - y < 0 or y > 20
            - z < 0 or z > 3
            - t < 0 or t > available prediction horizon

        Out-of-time-range:
            - t before t=0 → returns risk at t=0
            - t after horizon → returns 1.0 (safety default)
        """
```

### Concrete implementations

| Class | Source | Used in |
|-------|--------|---------|
| `FDSRiskMap` | Pre-computed FDS slices | Training data, EXP-RISK-001 ground truth |
| `FNORiskMap` | PI-FNO model inference | EXP-RISK-001 evaluation |
| `DynamicRiskMap` | Live PI-FNO + time advance | Week 12 PyBullet demo |

All three implement the same `query()` signature. Code that consumes
risk maps does not need to know which type is in use.

### Standard usage pattern

```python
# In data pipeline:
fds_map = FDSRiskMap.from_directory("data/raw/scenario_000")
danger = fds_map.query(np.array([15.0, 10.0, 1.5]), t=120.0)

# In PyBullet demo:
dyn_map = DynamicRiskMap(model_checkpoint, initial_state)
while sim_running:
    drone_pos, _ = pybullet.getBasePositionAndOrientation(drone_id)
    danger = dyn_map.query(np.array(drone_pos), t=current_t)
    # …  use danger to drive drone behaviour
```

---

## 3. Data Pipeline

### `fds_extractor.extract_slices`

```
Signature: extract_slices(fds_dir: Path) -> dict[str, np.ndarray]
```

**Returns** dict with keys:

| Key | Shape | Dtype | Units |
|-----|-------|-------|-------|
| `temperature` | (31, 60, 40, 6) | float32 | °C (raw) |
| `visibility`  | (31, 60, 40, 6) | float32 | m (raw) |
| `co_ppm`      | (31, 60, 40, 6) | float32 | ppm (raw) |
| `coords`      | dict | dict | metres |
| `times`       | (31,) | float32 | seconds |

`coords` sub-keys: `x` (60,), `y` (40,), `z` (6,).

Values are **un-normalised**. Normalisation happens in
`src/data_pipeline/normalize.py`.

### `mask_generator.generate_mask`

```
Signature: generate_mask(fds_dir: Path) -> np.ndarray
Returns  : shape (60, 40, 6) bool or float32
           1.0 = fluid (free), 0.0 = solid (wall)
```

The mask is identical across all scenarios (building geometry doesn't
change), so it is generated once and saved to `data/building_mask.npz`.

### `build_dataset.build`

```
Signature: build(scenario_dirs: list[Path], output_h5: Path) -> None
```

Output HDF5 structure:
```
dataset.h5
├── scenarios/
│   ├── scenario_000/
│   │   ├── input          shape (31, 5, 60, 40, 6)  normalised float32
│   │   └── target         shape (31, 3, 60, 40, 6)  normalised float32
│   ├── scenario_001/
│   └── ...
├── mask                   shape (60, 40, 6)
└── metadata               JSON-encoded scenario configs
```

---

## 4. FireDataset

```python
class FireDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        h5_path: Path,
        split: Literal["train", "val", "test_ood"],
    ): ...

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Returns:
            x: shape (5, 60, 40, 6)  — input at time t   (normalised)
            y: shape (3, 60, 40, 6)  — target at time t+1 (normalised)
        """

    def __len__(self) -> int:
        # Total pairs = sum over scenarios of (n_frames - 1)
        # For 24 train scenarios × 30 pairs/scenario = 720 pairs
```

---

## 5. PathPlanner Contract

```python
class EvacuationPlanner(ABC):
    @abstractmethod
    def plan(
        self,
        start_xyz: np.ndarray,
        risk_map: RiskMap,
        graph: nx.Graph,
        t: float = 0.0,
    ) -> list[np.ndarray]:
        """Compute safest path from start to nearest exit.

        Args:
            start_xyz: shape (3,) — occupant world position in metres.
            risk_map:  any RiskMap implementation.
            graph:     building NetworkX graph (16–20 nodes).
            t:         simulation time in seconds (for dynamic planners).

        Returns:
            Ordered list of waypoints (each shape (3,) world metres),
            from start to exit (inclusive).
            Returns empty list if no path exists.
        """
```

Three concrete implementations for EXP-PATH-001:

| Class | Strategy |
|-------|----------|
| `DijkstraPlanner` | Shortest path; ignores risk |
| `StaticAvoidancePlanner` | A* with current risk only; no re-planning |
| `DynamicPredictivePlanner` | A* with 60s predictive risk; re-plans every 30s |

### Building graph structure

NetworkX undirected graph with:

**Nodes** (16–20 total):
- Attributes: `pos: tuple[float, float, float]` in metres,
  `type: Literal["room", "corridor", "intersection", "exit"]`,
  `is_exit: bool`

**Edges**:
- Attributes: `length: float` (m), `width: float` (m),
  `base_time: float` (s, for walking at 1.5 m/s)

---

## 6. Evaluation Metrics

All metrics operate on **normalised** tensors:

| Metric | Function | Output shape |
|--------|----------|--------------|
| RMSE per channel | `metrics.rmse_per_channel` | (3,) |
| MAE per channel | `metrics.mae_per_channel` | (3,) |
| SSIM per channel | `metrics.ssim_per_channel` | (3,) |
| Peak danger error | `metrics.peak_danger_error` | scalar |
| FED error along path | `metrics.fed_error` | scalar |
| Reach time (evacuation) | `metrics.reach_time` | scalar (s) |

### Comparison reports

| Experiment | Compares | Output |
|------------|----------|--------|
| EXP-FIRE-001 | ConvLSTM vs PI-FNO no-PI vs PI-FNO full | `results/exp_fire_001/comparison.csv` |
| EXP-RISK-001 | FDS ground truth vs PI-FNO predicted risk maps | `results/exp_risk_001/...csv` |
| EXP-PATH-001 | Dijkstra vs Static vs Dynamic paths | `results/exp_path_001/...csv` |

---

## 7. Configuration File Conventions

All configs are YAML, loaded via dataclass.

```python
from dataclasses import dataclass

@dataclass
class TrainingConfig:
    learning_rate: float
    batch_size: int
    epochs: int
    # …
```

Config file paths follow the naming convention:

```
configs/
├── building.yaml          # Geometry constants
├── data.yaml              # FDS paths, normalisation
├── conv_lstm.yaml         # ConvLSTM hyperparams
├── pi_fno.yaml            # PI-FNO hyperparams
├── risk_map.yaml          # Tenability, FED weights
└── path_planning.yaml     # A* α/β, replan period
```

---

## 8. Versioning Policy

| Interface | Stable after |
|-----------|--------------|
| Tensor shapes | Week 8 |
| RiskMap.query signature | Week 12 |
| FireDataset return format | Week 8 |
| PathPlanner.plan signature | Week 11 |
| Evaluation metric outputs | Week 14 |

**Before changing a "stable" interface**, log the proposal in
`docs/decisions.md` and discuss before touching code.
