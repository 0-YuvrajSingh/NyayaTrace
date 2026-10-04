import json
try:
    data = json.load(open("/out/e1_test_predictions.json"))
    print("E1 Replay:", data.get("test_metrics"))
except Exception as e: print("E1 parse error:", e)

try:
    data2 = json.load(open("/out/e2_test_predictions.json"))
    print("E2 Replay:", data2.get("E2_chunk_and_pool", {}).get("test_metrics"))
except Exception as e: print("E2 parse error:", e)
