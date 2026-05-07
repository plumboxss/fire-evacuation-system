#!/usr/bin/env bash
# run_data_pipeline.sh — Extract FDS data and build the processed dataset.
# Usage: bash scripts/run_data_pipeline.sh [--raw-dir data/raw] [--output data/processed/dataset.h5]
# Implements Week 5–6. See docs/manual_v2.md.

set -euo pipefail

RAW_DIR="${RAW_DIR:-data/raw}"
OUTPUT="${OUTPUT:-data/processed/dataset.h5}"

echo "=== Data Pipeline ==="
echo "Raw dir : $RAW_DIR"
echo "Output  : $OUTPUT"

# Activate virtual environment if present
if [ -f ".venv/bin/activate" ]; then
    source ".venv/bin/activate"
fi

# Step 1: Verify raw data
echo ""
echo "[1/3] Verifying raw FDS scenarios ..."
python -c "
from pathlib import Path
raw = Path('$RAW_DIR')
scenarios = sorted([d for d in raw.iterdir() if d.is_dir()])
print(f'  Found {len(scenarios)} scenario directories')
if len(scenarios) < 1:
    raise SystemExit('ERROR: No scenario directories found in $RAW_DIR')
"

# Step 2: Build dataset
echo ""
echo "[2/3] Building processed dataset ..."
python -c "
from pathlib import Path
from src.data_pipeline.build_dataset import build
build(raw_dir=Path('$RAW_DIR'), output_path=Path('$OUTPUT'))
print('  Dataset built successfully.')
"

# Step 3: Verify processed dataset
echo ""
echo "[3/3] Verifying processed dataset ..."
python -c "
from pathlib import Path
from src.data_pipeline.verify import verify_dataset
ok = verify_dataset(Path('$OUTPUT'))
if not ok:
    raise SystemExit('ERROR: Dataset verification failed.')
print('  Verification passed.')
"

echo ""
echo "=== Data pipeline complete: $OUTPUT ==="
