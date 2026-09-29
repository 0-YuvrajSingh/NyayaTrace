import json
d = json.load(open("/out/e1_test.json"))
print("E1 metrics:")
print(json.dumps(d.get("test_metrics"), indent=2))
