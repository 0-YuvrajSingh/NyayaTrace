#!/bin/bash
set -e
mkdir -p /out/logs
echo "Installing base tools..."
apt-get update -qq && apt-get install -y -qq time procps 2>&1 >/dev/null

echo "Copying directories..."
mkdir -p /work/artifacts
find /repo/artifacts -mindepth 1 -maxdepth 1 ! -name 'e2_hf_cache' ! -name 'e2_chunk_pool_checkpoints_cached' -exec cp -r {} /work/artifacts/ \;

cp -r /repo/src /repo/scripts /repo/config /repo/answer_key /repo/validation_replay /repo/demo /repo/tests /work/
ln -s /repo/corpus /work/corpus
ln -s /repo/artifacts/e2_chunk_pool_checkpoints_cached /work/checkpoints || true

cd /work
export PYTHONPATH=/work/src
echo "PIP Install E1 and Testing..."
pip install -q joblib numpy scikit-learn==1.9.0 pyarrow==21.0.0 pydantic sqlmodel scipy httpx fastapi pytest pytest-asyncio 2>&1 | tee /out/logs/pip_e1.log

echo "--- D7: E1 Replay (No Torch) ---"
/usr/bin/time -v python scripts/reconstruct_e1_predictions.py --model-output /out/e1_model.joblib --predictions-output /out/e1_test.json 2>&1 | tee /out/logs/e1.log

echo "--- D10: Pytest ---"
PYTHONDONTWRITEBYTECODE=1 pytest -p no:cacheprovider -q 2>&1 | tee /out/logs/pytest.log || true
cd demo/ml-service
PYTHONDONTWRITEBYTECODE=1 pytest -p no:cacheprovider -q tests/ 2>&1 | tee /out/logs/pytest_fastapi.log || true
cd /work

echo "--- D5: BM25 Rebuild ---"
python scripts/build_bm25_index.py --corpus corpus/ecourts/cleaned --output /out/bm25.sqlite --manifest /out/bm25_index.json 2>&1 | tee /out/logs/bm25.log || true

echo "--- D5: Corpus Identity Rebuild ---"
python scripts/build_ecourts_corpus_identity.py --corpus corpus/ecourts/cleaned --output /out/ecourts_corpus_identity.json 2>&1 | tee /out/logs/corpus.log || true

echo "--- D8: E2 Setup ---"
pip install -q torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu 2>&1 | tee /out/logs/pip_torch.log
pip install -q accelerate==1.0.1 transformers==4.46.3 2>&1 | tee /out/logs/pip_e2.log

echo "--- D8: Environment Info ---"
free -m 2>&1 | tee /out/logs/free.log || true
docker info | grep Memory 2>&1 | tee /out/logs/docker_info.log || true
nvidia-smi 2>&1 | tee /out/logs/nvidia.log || true

echo "--- D8: E2 Replay ---"
/usr/bin/time -v python scripts/infer_e2_checkpoint_predictions.py --checkpoint /work/checkpoints/checkpoint-6318 --output /out/e2_test.json 2>&1 | tee /out/logs/e2.log

echo "DONE"
