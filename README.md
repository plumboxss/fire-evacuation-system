# Fire Evacuation Prediction System

Undergraduate engineering capstone: an active fire-response system that predicts
fire spread with deep learning and computes real-time evacuation paths.

## What It Does

1. **Fire prediction** — ConvLSTM and PI-FNO models, trained on FDS simulation
   data, predict temperature, visibility, and CO fields for the next 300 s.
2. **Risk mapping** — Predictions are converted to ISO-13571-based danger maps
   via tenability analysis.
3. **Evacuation routing** — Weighted A* on a 3-D grid graph finds the safest
   path from any occupant position to an exit.
4. **Integrated demo** (Week 12) — A single PyBullet drone follows the planned
   path in a simulated building.

## Key Constraints

- Single-floor building: 30 m × 20 m × 3 m
- Grid: 60 × 40 × 6 cells at 0.5 m resolution
- 30 FDS scenarios (24 train / 3 val / 3 OOD)
- GPU: NVIDIA A100 40 GB (RunPod)

## Project Structure

```
fire-evacuation-system/
├── configs/          YAML configs for models and pipeline
├── data/             Raw FDS outputs and processed tensors
├── src/
│   ├── shared/       Constants, normalization, coordinates
│   ├── data_pipeline/ FDS extraction → normalized tensors
│   ├── dataset/      PyTorch Dataset / DataModule
│   ├── models/       ConvLSTM3D, PI-FNO
│   ├── training/     Training loops and callbacks
│   ├── evaluation/   Metrics and model comparison
│   ├── risk_map/     ISO-13571 tenability → danger [0,1]
│   ├── path_planning/ Building graph + A* planner
│   ├── integration/  Week-12 PyBullet demo (team member D)
│   └── visualization/ Plotting utilities
├── experiments/      Standalone experiment scripts
├── tests/            pytest suite
├── docs/             Coordinate conventions, interface contracts
└── scripts/          Setup and run scripts
```

## Quickstart

```bash
# 1. Create environment and install dependencies
bash scripts/setup_env.sh

# 2. Verify constants and normalization
python -m src.shared.constants
python -m src.shared.normalization

# 3. Run tests
pytest tests/test_constants.py tests/test_normalization.py -v

# 4. (After data download) Build dataset
bash scripts/run_data_pipeline.sh
```

## Tech Stack

Python 3.10 · PyTorch 2.0 · neuraloperator · fdsreader · NetworkX · W&B · pytest

## Documentation

- [`docs/coordinate_convention.md`](docs/coordinate_convention.md)
- [`docs/risk_indicators.md`](docs/risk_indicators.md)
- [`docs/interface_contracts.md`](docs/interface_contracts.md)
- [`docs/manual_v2.md`](docs/manual_v2.md) *(user-populated)*
- [`CLAUDE.md`](CLAUDE.md) — full project context for AI-assisted development
