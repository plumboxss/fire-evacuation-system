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
Range  : [0, 1]  (all channels)
Device : CUDA (training) / CPU (inference)
```

Channel layout (dimension 1):

| Index | Name | Raw unit | Normalization |
|-------|------|----------|---------------|
| 0 | Temperature | °C | `(T − 20) / 1180`, clipped [0,1] |
| 1 | Visibility | m | `1 − clip(V/30, 0, 1)` **INVERSE** |
| 2 | CO | ppm | `log1p(CO) / log1p(5000)`, clipped [0,1] |
| 3 | Mask | — | 1.0 = fluid cell, 0.0 = solid (wall) |
| 4 | Time encoding | — | `t / T_end ∈ [0, 1]`, broadcast to grid |

Convention: **higher value = more dangerous** for channels 0–2.

### Output Tensor

```
Shape  : (B, 3, 60, 40, 6)
Dtype  : torch.float32
Range  : [0, 1]
```

Channel layout (dimension 1):

| Index | Name | Same normalization as input |
|-------|------|-----------------------------|
| 0 | Temperature | Yes |
| 1 | Visibility | Yes (inverse) |
| 2 | CO | Yes |

---

## 2. RiskMap Contract

```python
from abc import ABC, abstractmethod
import numpy as np

class RiskMap(ABC):
    @abstractmethod
    def query(self, xyz: np.ndarray, t: float | None = None) -> float:
        """Return danger level at world coordinate xyz = (x, y, z) in metres.

        Args:
            xyz: 1-D array of length 3: [x_m, y_m, z_m].
            t:   Query time in seconds. If None, uses the latest available frame.

        Returns:
            Danger level ∈ [0, 1].
            Returns **1.0** (maximum danger) for out-of-bounds coordinates.
            Returns **1.0** if t is beyond the available prediction horizon.
        """
```

Concrete implementations in `src/risk_map/`:
- `StaticRiskMap` — wraps a pre-computed (T, 60, 40, 6) array.
- `PredictiveRiskMap` — queries the live model and caches results.

---

## 3. Data Pipeline

### `fds_extractor.extract_slices`

```
Input  : Path to a directory containing FDS *.smv and slice files
Output : Dict[str, np.ndarray]
         Keys: "temperature", "visibility", "co_ppm"
         Values shape: (31, 60, 40, 6)  — (time, nx, ny, nz)
         Units: °C, m, ppm  (raw, un-normalised)
```

### `build_dataset.build`

```
Input  : List of scenario directories (raw FDS outputs)
Output : HDF5 file at data/processed/dataset.h5
         Group structure:
           /scenario_{i:03d}/input   shape (31, 5, 60, 40, 6)  normalised
           /scenario_{i:03d}/target  shape (31, 3, 60, 40, 6)  normalised
```

---

## 4. FireDataset

```python
class FireDataset(torch.utils.data.Dataset):
    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Returns:
            x: (5, 60, 40, 6)  — single-frame model input (normalised)
            y: (3, 60, 40, 6)  — single-frame target (normalised)
        """
```

Pairs are (frame t, frame t+1): model predicts the next state.

---

## 5. Path Planner

```python
class EvacuationPlanner:
    def plan(
        self,
        start_xyz: np.ndarray,
        risk_map: RiskMap,
        t: float,
    ) -> list[np.ndarray]:
        """Compute safest path from start to nearest exit.

        Args:
            start_xyz: Occupant world position (x, y, z) in metres.
            risk_map:  Risk map to query for edge weights.
            t:         Current simulation time in seconds.

        Returns:
            Ordered list of world-space waypoints (x, y, z) in metres,
            from start to exit (inclusive).
            Returns empty list if no path exists.
        """
```

---

## 6. Evaluation Metrics

All metrics operate on **normalised** tensors:

| Metric | Function | Shape |
|--------|----------|-------|
| RMSE per channel | `metrics.rmse_per_channel` | (3,) |
| MAE per channel | `metrics.mae_per_channel` | (3,) |
| SSIM per channel | `metrics.ssim_per_channel` | (3,) |
| Peak danger error | `metrics.peak_danger_error` | scalar |
| FED error | `metrics.fed_error` | scalar |

---

## 7. Versioning Policy

- Interface changes must be discussed and reflected in this document first.
- Tensor shapes are considered **stable** after Week 8.
- The `RiskMap.query` signature is **frozen** after Week 12.
