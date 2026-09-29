import json, os, stat, datetime

print("--- ITEM 2: FREEZE_RECONCILIATION.md ---")
print(open("/repo/experiments/audit_fixes/FREEZE_RECONCILIATION.md").read())

print("--- ITEM 2: hash_table.md ---")
content = open("/repo/experiments/audit_fixes/hash_table.md", encoding="utf-16").read()
print(content)
print(f"(hash_table.md row count, excluding headers: {len(content.strip().split(chr(10)))-2})")

print("--- ITEM 2: docs/freeze_drift_audit.md table rows ---")
audit_content = open("/repo/docs/freeze_drift_audit.md").read()
for line in audit_content.split('\n'):
    if line.startswith('|') and '`' in line:
        print(line)

print("\n--- ITEM 3: Duplicated paths in config ---")
data = json.load(open("/repo/config/reproducibility_freeze.json"))
path_map = {}
def recurse(obj, parent_key="root"):
    if isinstance(obj, dict):
        if 'path' in obj and 'sha256' in obj:
            p = obj['path']
            if p not in path_map: path_map[p] = []
            path_map[p].append((parent_key, obj['sha256']))
        for k, v in obj.items(): recurse(v, k)
    elif isinstance(obj, list):
        for i, item in enumerate(obj): recurse(item, f"{parent_key}[{i}]")
recurse(data)
for p, entries in path_map.items():
    if len(entries) > 1:
        print(f"Path: {p}")
        for entry in entries:
            print(f"  Parent Key: {entry[0]}, Hash: {entry[1]}")

print("\n--- ITEM 4: 9 DRIFT files ---")
drift_files = [
    "artifacts/bm25_index.json",
    "artifacts/e1_baseline_results.json",
    "artifacts/e2_correction_manifest.json",
    "artifacts/e3_e4_evidence_augmented_evaluation.json",
    "artifacts/e3_e4_prediction_error_analysis.json",
    "artifacts/ecourts_corpus_identity.json",
    "artifacts/week10_dev_probe_selfmatch_recheck.json",
    "artifacts/week10_post_selfmatch_freeze_regression.json",
    "artifacts/week11_temporal_prerank_evaluation.json"
]
freeze_config_mtime = os.stat("/repo/config/reproducibility_freeze.json").st_mtime
print(f"config/reproducibility_freeze.json mtime: {datetime.datetime.fromtimestamp(freeze_config_mtime)}")
for line in open("/repo/docs/freeze_drift_audit.md").readlines():
    if "Audit Date:" in line:
        print(f"week10_reproducibility_freeze.md / docs date: {line.strip()}")
        break

for f in drift_files:
    full = "/repo/" + f
    if not os.path.exists(full): continue
    st = os.stat(full)
    sz = st.st_size
    mt = datetime.datetime.fromtimestamp(st.st_mtime)
    print(f"\n- {f} (Size: {sz}, mtime: {mt})")
    try:
        j = json.load(open(full))
        meta_keys = ['built_at_utc', 'versions', 'evaluation_version', 'timestamp', 'artifact_version', 'identity_version', 'analysis_version', 'index_version']
        found = False
        for mk in meta_keys:
            if mk in j:
                print(f"  {mk}: {j[mk]}")
                found = True
        if not found:
            print("  No common timestamp/version fields found at top level.")
    except: pass

print("\n--- ITEM 6: 1503 vs 1517 eligibility filter ---")
import ast
class ASTVisitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        if 'eligib' in node.name.lower() or 'filter' in node.name.lower():
            print(f"Found func {node.name} in analyze_e1_exclusions.py or similar")
            # We will just grep for it instead
        self.generic_visit(node)
