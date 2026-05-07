#!/usr/bin/env bash
# run_experiments.sh — Run all named experiments sequentially.
# Usage: bash scripts/run_experiments.sh [--conv-lstm CKPT] [--pi-fno CKPT]
# Implements Week 14. See docs/manual_v2.md.

set -euo pipefail

CONV_LSTM_CKPT="${CONV_LSTM_CKPT:-checkpoints/conv_lstm/best.pt}"
PI_FNO_CKPT="${PI_FNO_CKPT:-checkpoints/pi_fno/best.pt}"
DATA="${DATA:-data/processed/dataset.h5}"

if [ -f ".venv/bin/activate" ]; then
    source ".venv/bin/activate"
fi

echo "=== Running Experiments ==="

echo ""
echo "[1/3] exp_fire_001_compare_models ..."
python experiments/exp_fire_001_compare_models.py \
    --conv-lstm "$CONV_LSTM_CKPT" \
    --pi-fno    "$PI_FNO_CKPT" \
    --data      "$DATA"

echo ""
echo "[2/3] exp_risk_001_validate_map ..."
python experiments/exp_risk_001_validate_map.py \
    --checkpoint "$PI_FNO_CKPT" \
    --data       "$DATA"

echo ""
echo "[3/3] exp_path_001_compare_paths ..."
python experiments/exp_path_001_compare_paths.py \
    --checkpoint "$PI_FNO_CKPT" \
    --data       "$DATA"

echo ""
echo "=== All experiments complete. Results in results/ ==="
