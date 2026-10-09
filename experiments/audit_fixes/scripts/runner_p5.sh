#!/bin/bash
set -e
mkdir -p /out/logs
echo "--- Starting P5 Runner ---"

echo "Copying repo to /work..."
mkdir -p /work
cp -r /repo/src /repo/scripts /repo/config /repo/answer_key /repo/artifacts /repo/corpus /repo/validation_replay /repo/demo /repo/tests /work/
cp -r /repo/artifacts/e2_chunk_pool_checkpoints_cached /work/checkpoints || true

cd /work
export PYTHONPATH=/work/src

echo "Installing pip dependencies..."
pip install -q joblib numpy pydantic sqlmodel scipy httpx fastapi pytest pytest-asyncio 2>&1 | tee /out/logs/pip_base.log
pip install -q scikit-learn==1.5.2 pyarrow==18.1.0 2>&1 | tee /out/logs/pip_e1.log

echo "--- D7: E1 Replay (No Torch) ---"
/usr/bin/time -v python scripts/reconstruct_e1_predictions.py --model-output /out/e1_model.joblib --predictions-output /out/e1_test.json 2>&1 | tee /out/logs/e1.log

echo "--- D10: Pytest ---"
PYTHONDONTWRITEBYTECODE=1 pytest -p no:cacheprovider -q 2>&1 | tee /out/logs/pytest.log || true

echo "--- D10: FastAPI Tests ---"
cd /work/demo/ml-service
PYTHONDONTWRITEBYTECODE=1 pytest -p no:cacheprovider -q tests/ 2>&1 | tee /out/logs/pytest_fastapi.log || true
cd /work

echo "--- D8: E2 Replay Setup (CPU Torch) ---"
pip install -q torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu 2>&1 | tee /out/logs/pip_torch.log
pip install -q accelerate==1.0.1 transformers==4.46.3 2>&1 | tee /out/logs/pip_e2.log

echo "--- D12: Environment Info ---"
free -m 2>&1 | tee /out/logs/free.log || true
docker info | grep Memory 2>&1 | tee /out/logs/docker_info.log || true
nvidia-smi 2>&1 | tee /out/logs/nvidia.log || true

echo "--- D8: E2 Replay ---"
/usr/bin/time -v python scripts/infer_e2_checkpoint_predictions.py --checkpoint /work/checkpoints/checkpoint-6318 --output /out/e2_test.json 2>&1 | tee /out/logs/e2.log

echo "--- D5: BM25 & Corpus Identity Rebuild ---"
python scripts/build_bm25_index.py --corpus /work/corpus/ecourts/cleaned --output /out/bm25.sqlite --manifest /out/bm25_index.json 2>&1 | tee /out/logs/bm25_rebuild.log || true
python scripts/build_ecourts_corpus_identity.py --corpus /work/corpus/ecourts/cleaned --output /out/ecourts_corpus_identity.json 2>&1 | tee /out/logs/corpus_identity.log || true

echo "Runner script complete."
