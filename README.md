# Fire Evacuation Prediction System

> **14-week undergraduate engineering capstone competition entry.**
> Active fire-response system using physics-informed neural operators
> and dynamic path planning.

---

## What This Project Does

End-to-end pipeline:

```
FDS simulation data
   ↓
ConvLSTM and PI-FNO models predict fire spread
(Temperature, Visibility, CO over 60s horizon)
   ↓
ISO-13571-based risk map conversion
(Tenability thresholds + cumulative FED)
   ↓
Weighted A* on building graph
(Static baseline vs Dynamic predictive)
   ↓
Path safety validation (EXP-PATH-001)
   ↓
PyBullet integrated demo (Week 12)
```

---

## Six Hypotheses Driving the Project

| ID | Hypothesis | Validates |
|----|-----------|-----------|
| H1 | PI-FNO ≥1000× faster than FDS | EXP-FIRE-001 |
| H2 | Relative L2 ≤15% on val | EXP-FIRE-001 |
| H3 | PI-FNO outperforms ConvLSTM on OOD | EXP-FIRE-001 |
| H4 | Risk map FNR <10% | EXP-RISK-001 |
| H5 | Risk map IoU ≥0.7 vs FDS GT | EXP-RISK-001 |
| **H6** | **Dynamic A* reduces FED ≥30% vs static** | **EXP-PATH-001** |

H6 is the headline result. See `docs/manual_v2.md` for full hypothesis
discussion and presentation order.

---

## Key Constraints

| Item | Value |
|------|-------|
| Building | Single-floor maze layout, 3 exits |
| STL height | Up to **3.2 m** (preserved as physical geometry) |
| FDS MESH | 100 × 80 × 8 cells over [−10, 40] × [−10, 30] × [0, 4] m |
| **SLCF (model-visible)** | **60 × 40 × 6 cells over [0, 30] × [0, 20] × [0, 3] m** |
| Cell resolution | 0.5 m × 0.5 m × 0.5 m |
| Time | 0–300 s, 31 frames at 10 s |
| Training data | 30 FDS scenarios (24 / 3 / 3) |
| GPU | NVIDIA A100 40 GB on RunPod |
| Units | **SI only** (m, s, °C, ppm) |

For the rationale behind each constraint, see `docs/decisions.md`.

---

## Team Roles

| Member | Owns |
|--------|------|
| **A** | PyroSim modeling, FDS simulations |
| **B** | ConvLSTM, PI-FNO training |
| **C** | Data pipeline, dataset, normalization |
| **D** | Evaluation, integration, visualization, paper |

Risk map and path planning (Weeks 10–11) are joint B+C work.

---

## Project Structure

```
fire-evacuation-system/
├── CLAUDE.md                ← AI context file (read first)
├── README.md                ← this file
├── pyproject.toml           ← package metadata
├── requirements.txt         ← Python dependencies
├── .gitignore
├── configs/                 ← YAML hyperparameters per module
│   ├── building.yaml
│   ├── data.yaml
│   ├── conv_lstm.yaml
│   ├── pi_fno.yaml
│   ├── risk_map.yaml
│   └── path_planning.yaml
├── data/
│   ├── raw/                 ← FDS outputs (gitignored, large)
│   └── processed/           ← .h5 dataset (gitignored)
├── src/
│   ├── shared/              ← constants, normalization, coordinates, building
│   ├── data_pipeline/       ← FDS .smv/.sf → .npz/.h5 conversion (Week 6)
│   ├── dataset/             ← PyTorch Dataset (Week 6)
│   ├── models/              ← ConvLSTM3D, PI-FNO, base classes (Week 7-9)
│   ├── training/            ← training loops, callbacks (Week 7-9)
│   ├── evaluation/          ← metrics, comparisons (Week 9-10)
│   ├── risk_map/            ← tenability, FED, ASET, RiskMap classes (Week 10)
│   ├── path_planning/       ← graph, A*, evacuation simulator (Week 11)
│   ├── integration/         ← PyBullet demo (Week 12)
│   └── visualization/       ← plots, animations (Week 13)
├── experiments/             ← exp_fire_001, exp_risk_001, exp_path_001
├── tests/                   ← pytest unit tests
├── notebooks/               ← exploratory analysis (not production)
├── docs/                    ← project documentation (the heart)
│   ├── manual_v2.md
│   ├── coordinate_convention.md
│   ├── risk_indicators.md
│   ├── interface_contracts.md
│   ├── decisions.md
│   ├── lessons_learned.md
│   └── task_request_template.md
├── checkpoints/             ← trained models (gitignored)
├── results/                 ← experiment outputs (CSV, JSON)
├── figures/                 ← paper/slide figures
└── scripts/                 ← bash helpers (setup, run pipeline, etc.)
```

---

## Three Critical Experiments

The whole project is structured around three named experiments.

| Experiment | Compares | Output |
|------------|----------|--------|
| **EXP-FIRE-001** | ConvLSTM vs FNO no-PI vs FNO full | `results/exp_fire_001/comparison.csv` |
| **EXP-RISK-001** | FDS ground truth vs PI-FNO risk maps | `results/exp_risk_001/comparison.csv` |
| **EXP-PATH-001** | Dijkstra vs Static vs Dynamic planners | `results/exp_path_001/comparison.csv` |

Plus three ablations on PI loss components, training data size, and
(optionally) model size. See `docs/manual_v2.md` for full schedule.

---

## Quickstart

### Initial setup (Week 1, once)

```bash
# 1. Clone and enter
git clone <your-repo-url> fire-evacuation-system
cd fire-evacuation-system

# 2. Create environment and install dependencies
bash scripts/setup_env.sh

# 3. Verify foundation modules work
python -m src.shared.constants            # → PASS
python -m src.shared.normalization        # → PASS
python -m src.shared.coordinates          # → PASS
pytest tests/test_constants.py tests/test_normalization.py -v
```

### After FDS data is generated (Week 5–6)

```bash
# Build dataset from raw FDS outputs
bash scripts/run_data_pipeline.sh

# Verify dataset
python -m src.dataset.fire_dataset
```

### Training (Week 7+)

```bash
# Train ConvLSTM baseline
python -m src.training.train_conv_lstm --config configs/conv_lstm.yaml

# Train PI-FNO (after Week 8)
python -m src.training.train_fno --config configs/pi_fno.yaml
```

### Run experiments (Week 9–12)

```bash
# Compare three models (EXP-FIRE-001)
python experiments/exp_fire_001_compare_models.py

# Compare three planners (EXP-PATH-001, the H6 test)
python experiments/exp_path_001_compare_paths.py
```

---

## For Claude Code Sessions

**Read first**: `CLAUDE.md` (auto-loaded by Claude Code in this directory)

**For specific tasks**: see `docs/task_request_template.md` for the
8-section format used to delegate work to Claude Code.

**For decisions**: `docs/decisions.md` — past decisions are append-only.
Don't reverse a decision without a new entry.

**For known bugs**: `docs/lessons_learned.md` — check before claiming
"this seems weird, let me investigate."

---

## Tech Stack

Python 3.10+ · PyTorch 2.0+ · CUDA 11.8+ · neuraloperator · fdsreader ·
NetworkX · scipy · pybullet · gym-pybullet-drones · Weights & Biases · pytest

---

## Documentation Map

| Document | Purpose | When to read |
|----------|---------|--------------|
| `CLAUDE.md` | Project context for AI sessions | Always (auto-loaded) |
| `docs/manual_v2.md` | 14-week schedule with all phases | Planning a week of work |
| `docs/interface_contracts.md` | Exact function signatures, tensor shapes | Implementing a module |
| `docs/coordinate_convention.md` | Coordinate system rules | Anything spatial (FDS, geometry, drones) |
| `docs/risk_indicators.md` | ISO 13571, FED, ASET formulas | Risk map work (Week 10) |
| `docs/decisions.md` | Why we made past choices (D-001 .. D-018) | Considering a re-design |
| `docs/lessons_learned.md` | Bugs already encountered (L-001 .. L-011) | Debugging |
| `docs/task_request_template.md` | How to write Claude Code tasks | Delegating work |

---

## Status (Current Project State)

Update this section as the project progresses.

**Last data validation**: `0507_v1` simulation has SLCF Z=3.5 issue.
Awaiting re-simulation with SLCF Z=3.0 fix (see L-009).

**Next milestone**: Validate fdsreader on corrected single-scenario data,
then implement `src/data_pipeline/fds_extractor.py` (Week 6 work).

**Known issues in pipeline**:
- STL units in mm (need conversion before PyroSim import) — see L-010
- SLCF Z range must be `0,3` exactly (PyroSim defaults to 3.5) — see L-009

**Completed milestones**:
- ✅ Skeleton repo created
- ✅ Foundation context files (CLAUDE.md, docs/) drafted
- ✅ ConvLSTM 3D model implemented and validated (349k params)
- ⏳ FDS data validation in progress

---

## License

MIT (assumed for capstone; check competition rules before public release).

---

## Contributing

This is a closed-team project for a competition entry. After Week 14
the codebase will be open-sourced for academic reproducibility.

For team members: see `docs/manual_v2.md` for week-by-week task
allocation and `docs/task_request_template.md` for how to delegate
to Claude Code.
