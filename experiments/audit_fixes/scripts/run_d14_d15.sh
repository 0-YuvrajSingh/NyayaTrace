#!/bin/bash
set -e

echo "--- D12: Machine Info ---"
nproc
free -m || true
docker info | grep Memory || true
nvidia-smi || true

echo "--- Setup ---"
apt-get update -qq && apt-get install -y -qq time procps
pip install -q joblib numpy scikit-learn transformers pydantic sqlmodel scipy pyarrow httpx fastapi pytest
# CPU-only torch
pip install -q torch accelerate --index-url https://download.pytorch.org/whl/cpu

mkdir -p /work
echo "Copying to /work..."
cp -r /repo/src /repo/scripts /repo/config /repo/answer_key /repo/artifacts /repo/corpus /repo/validation_replay /repo/demo /repo/tests /work/
cp -r /repo/artifacts/e2_chunk_pool_checkpoints_cached /work/checkpoints || true

cd /work
export PYTHONPATH=/work/src

echo "--- D13: E1 Replay ---"
/usr/bin/time -v python scripts/reconstruct_e1_predictions.py --model-output /work/e1_reconstructed_model.joblib --predictions-output /work/e1_test_predictions.json

echo "--- D13: E2 Replay ---"
/usr/bin/time -v python scripts/infer_e2_checkpoint_predictions.py --checkpoint /work/checkpoints/checkpoint-6318 --output /work/e2_test_predictions.json

echo "--- D15: Pytest ---"
PYTHONDONTWRITEBYTECODE=1 pytest -p no:cacheprovider -q || true

echo "--- D15: FastAPI Tests ---"
cd /work/demo/ml-service
PYTHONDONTWRITEBYTECODE=1 pytest -p no:cacheprovider -q tests/ || true
