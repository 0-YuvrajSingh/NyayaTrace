# Demo ML-service image. Separate from the frozen E2 training image
# (docker/e2.Dockerfile), which must not be altered for scientific work.
FROM python:3.11-slim

WORKDIR /workspace
ENV PYTHONPATH=/workspace/src:/workspace/demo/ml-service
ENV HF_HOME=/workspace/artifacts/e2_hf_cache
ENV HF_HUB_DISABLE_TELEMETRY=1

COPY demo/ml-service/requirements.txt /workspace/demo/ml-service/requirements.txt
RUN pip install --no-cache-dir -r /workspace/demo/ml-service/requirements.txt

COPY src/ /workspace/src/
COPY config/ /workspace/config/
COPY demo/ml-service/app.py /workspace/demo/ml-service/app.py

EXPOSE 8001
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
