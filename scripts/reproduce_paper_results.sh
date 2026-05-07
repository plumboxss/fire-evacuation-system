#!/usr/bin/env bash
# reproduce_paper_results.sh — Full end-to-end reproduction of all paper results.
# WARNING: Requires a trained model checkpoint. Runs on A100 GPU.
# Usage: bash scripts/reproduce_paper_results.sh
# Implements Week 14. See docs/manual_v2.md.

set -euo pipefail

echo "=== Reproduce Paper Results ==="
echo "This script assumes:"
echo "  1. Raw FDS data is present in data/raw/"
echo "  2. A virtual environment is set up via scripts/setup_env.sh"
echo "  3. GPU (A100 40GB) is available"
echo ""

if [ -f ".venv/bin/activate" ]; then
    source ".venv/bin/activate"
fi

# Step 1: Build dataset
echo "[Step 1/5] Building dataset ..."
bash scripts/run_data_pipeline.sh

# Step 2: Train ConvLSTM
echo "[Step 2/5] Training ConvLSTM3D ..."
python -m src.training.train_conv_lstm \
    --config configs/conv_lstm.yaml \
    --data   data/processed/dataset.h5

# Step 3: Train PI-FNO
echo "[Step 3/5] Training PI-FNO ..."
python -m src.training.train_fno \
    --config configs/pi_fno.yaml \
    --data   data/processed/dataset.h5

# Step 4: Run all experiments
echo "[Step 4/5] Running experiments ..."
bash scripts/run_experiments.sh

# Step 5: Ablations
echo "[Step 5/5] Running ablations ..."
python experiments/ablation_pi_losses.py
python experiments/ablation_data_size.py
python experiments/ablation_model_size.py

echo ""
echo "=== Reproduction complete. Check results/ and figures/ ==="
