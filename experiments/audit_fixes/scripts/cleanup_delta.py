"""Compare before/after cleanup scans (read-only; writes delta reports)."""
import csv
import json
from pathlib import Path

BASE = Path("/out/project_cleanup_scan")
AFTER = Path("/out/project_cleanup_scan_after_g1_g4")


def load_inv(path):
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    return {r["path"]: r for r in rows}


before = load_inv(BASE / "01_full_inventory.csv")
after = load_inv(AFTER / "01_full_inventory.csv")
bp, ap = set(before), set(after)
removed = sorted(bp - ap)
added = sorted(ap - bp)

b_bytes = sum(int(v["size"]) for v in before.values() if int(v["size"]) > 0)
a_bytes = sum(int(v["size"]) for v in after.values() if int(v["size"]) > 0)

bd = json.load(open(BASE / "_dup_groups.json"))
ad = json.load(open(AFTER / "_dup_groups.json"))

lines = []
lines.append("# Cleanup delta report (G1-G4)")
lines.append("")
lines.append(f"1. File count: {len(before)} -> {len(after)} (delta {len(after) - len(before)})")
lines.append(f"2. Total bytes: {b_bytes} -> {a_bytes} (delta {a_bytes - b_bytes})")
bdirs = {p.rsplit("/", 1)[0] if "/" in p else "." for p in bp}
adirs = {p.rsplit("/", 1)[0] if "/" in p else "." for p in ap}
lines.append(f"3. Directory count: {len(bdirs)} -> {len(adirs)} (delta {len(adirs) - len(bdirs)})")
lines.append(f"4. Exact dup groups: {len(bd)} -> {len(ad)} (delta {len(ad) - len(bd)})")
lines.append("5. Near-duplicates: recheck below (paper variants + script pairs intact expected)")
def exts(inv):
    from collections import Counter
    c = Counter(v["ext"] for v in inv.values())
    return dict(c.most_common(8))
lines.append(f"6. Generated/temp: before ext {exts(before)}")
lines.append(f"   after ext {exts(after)}")
lines.append(f"11. Added files ({len(added)}):")
for p in added[:40]:
    lines.append(f"    + {p}")
lines.append(f"12. Removed files ({len(removed)}): expected G1+G2+G3+G4 only")
unexpected = [p for p in removed if not (
    p.startswith("experiments/audit_fixes/replay/spring-api-copy/") or
    p.startswith("demo/web/node_modules/") or
    p.startswith("demo/spring-api/target/") or
    "paper_master_" in p and p.split(".")[-1] in ("aux", "log", "out") or
    p.startswith("experiments/audit_fixes/replay/final") and p.endswith("_pass1.log") or
    p.startswith("experiments/audit_fixes/replay/final") and p.endswith("_pass2.log") or
    p.startswith("experiments/audit_fixes/replay/sixpage") and "pass" in p or
    p.startswith("experiments/audit_fixes/replay/latex_pass") or
    p == "experiments/audit_fixes/replay/logs/docker_info.log")]
lines.append(f"    unexpected removals: {unexpected if unexpected else 'NONE'}")
(AFTER / "cleanup_delta_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines[:12]))
print("unexpected:", unexpected if unexpected else "NONE")
