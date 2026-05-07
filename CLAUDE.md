# Fire Evacuation Prediction System — Project Context

> **Read this file first.** It is the single source of truth for project constraints,
> conventions, and scope. Never violate the hard constraints below.

---

## What This Project Is

14-week undergraduate capstone: an **active fire-response system**.

- **ConvLSTM** and **PI-FNO** models trained on FDS simulation data predict fire spread.
- Predictions are converted to **ISO-13571-based risk maps**.
- **Weighted A\*** computes dynamic evacuation paths.
- **PyBullet** is used in Week 12 for an integrated drone demo.

---

## Hard Constraints — NEVER Violate

| Parameter | Value |
|-----------|-------|
| Building | Single-floor only: **30 m × 20 m × 3 m** |
| Grid | **60 × 40 × 6 cells**, 0.5 m resolution. NEVER 0.2 m or different size. |
| Time | 0–300 s, **31 frames** at **10 s** intervals |
| Training data | Maximum **30 FDS scenarios** (24 train / 3 val / 3 OOD) |
| GPU | NVIDIA A100 40 GB on RunPod |
| Coordinate system | Meters, Z-up, origin at corner (0, 0, 0) |
| Units | **SI only** (meters, seconds, °C, ppm). NEVER mm. |

---

## Tech Stack

| Layer | Library / Tool |
|-------|---------------|
| Deep learning | Python 3.10+, PyTorch 2.0+, CUDA 11.8+ |
| Neural operator | `neuraloperator` (FNO) |
| FDS data | `fdsreader` |
| Graph / routing | `NetworkX` |
| Interpolation | `scipy` |
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

- All channels normalized to **[0, 1]**, convention: **higher = more dangerous**
- Visibility is **INVERSE-mapped**: low visibility → high value

---

## Risk Map Interface

```python
class RiskMap:  # abstract
    def query(self, xyz: np.ndarray, t: float = None) -> float:
        """
        Returns danger ∈ [0, 1] at world coordinate (x, y, z) in meters.
        Out-of-bounds returns 1.0 (max danger — safety default).
        """
```

---

## Tenability Thresholds (ISO 13571 + SFPE Handbook)

| Indicator | Safe | Danger |
|-----------|------|--------|
| Temperature | 30 °C | 60 °C |
| Visibility | 10 m (safe) | 3 m (danger) |
| CO instantaneous | 100 ppm | 1400 ppm |
| FED (CO cumulative) | — | 0.3 (sensitive population) |

---

## What This Project Does NOT Do

Do **not** add these features, even if they seem natural extensions:

- Multi-floor buildings
- Real-time CFD (FDS is pre-computed only)
- 0.2 m mesh resolution
- Drone swarms (single drone only)
- Real fire experiments (simulation only)
- Ventilation variation (all scenarios: both doors open)
- HCN or irritant gas FED (CO only)
- Real human behaviour modelling

---

## Coding Conventions

- All **public functions**: type hints + docstring **REQUIRED**
- Tensor shapes documented in docstrings
- File paths: **`pathlib.Path`**, never `os.path.join`
- Errors: `raise ValueError("clear message")`, never silent failures
- Computational modules **MUST** include `if __name__ == '__main__'` self-test
- Config files: **YAML** (not JSON, not Python dict)
- **Dataclass or Pydantic** for typed config objects (not raw dicts)
- Absolute imports: `from src.shared.constants import GRID_SHAPE`

---

## 14-Week Schedule Reference

| Week | Module |
|------|--------|
| 1–2  | Environment setup, FDS data download |
| 3–4  | Coordinate system, building geometry (`src/shared/`) |
| 5–6  | Data pipeline: extraction, normalization, masks (`src/data_pipeline/`) |
| 7–8  | Dataset class, DataModule (`src/dataset/`) |
| 9–10 | ConvLSTM training (`src/models/conv_lstm_3d.py`, `src/training/`) |
| 11   | PI-FNO training (`src/models/fno.py`, `src/training/train_fno.py`) |
| 12   | Risk map + path planning (`src/risk_map/`, `src/path_planning/`) |
| 13   | PyBullet integration demo (`src/integration/`) |
| 14   | Evaluation, figures, report (`src/evaluation/`, `src/visualization/`) |

---

## Key File Locations

| What | Where |
|------|-------|
| All numerical constants | `src/shared/constants.py` |
| Normalization functions | `src/shared/normalization.py` |
| Coordinate utilities | `src/shared/coordinates.py` |
| Building geometry | `src/shared/building.py` |
| Risk map abstract base | `src/risk_map/risk_map_class.py` |
| Interface contracts | `docs/interface_contracts.md` |
| Coordinate conventions | `docs/coordinate_convention.md` |
| Tenability reference | `docs/risk_indicators.md` |
