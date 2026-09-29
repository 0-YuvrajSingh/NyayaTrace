"""Timed E2 repeat: wall time + peak RSS via resource module (no GNU time needed)."""
import json
import resource
import subprocess
import sys
import time

start = time.time()
proc = subprocess.run(
    [sys.executable, "scripts/infer_e2_checkpoint_predictions.py",
     "--cache-dir", "/cache/test",
     "--checkpoint", "artifacts/e2_chunk_pool_checkpoints_cached/checkpoint-6318",
     "--recorded-result", "artifacts/e2_chunk_pool_results.json",
     "--output", "/out/e2_test_predictions_repeat.json",
     "--batch-size", "8"],
    check=False, capture_output=True, text=True,
)
wall = time.time() - start
print(proc.stdout[-2000:])
print(proc.stderr[-1000:], file=sys.stderr)
peak_kb = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
print(json.dumps({"exit": proc.returncode, "wall_seconds": round(wall, 2),
                  "max_rss_kb_child": peak_kb,
                  "max_rss_mb_child": round(peak_kb / 1024, 1)}, indent=2))
if proc.returncode != 0:
    raise SystemExit(proc.returncode)
# Determinism check vs first replay
a = json.load(open("/out/e2_test_predictions.json"))
b = json.load(open("/out/e2_test_predictions_repeat.json"))
print("repeat vs first-replay records identical:", a["records"] == b["records"])
print("repeat vs first-replay mean metrics identical:",
      a["mean_logits_metrics"] == b["mean_logits_metrics"])
