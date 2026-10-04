"""Full repo inventory (read-only /repo, writes only to /out scan dir)."""
import csv
import hashlib
import json
import os
import subprocess
from pathlib import Path

REPO = Path("/repo")
OUT = Path("/out/project_cleanup_scan_after_g1_g4")
OUT.mkdir(parents=True, exist_ok=True)

tracked = set()
try:
    r = subprocess.run(["git", "-C", "/repo", "ls-files"], capture_output=True, text=True, timeout=60)
    tracked = set(r.stdout.splitlines())
except Exception as e:
    print("git ls-files failed:", e)

ignored = set()
try:
    r = subprocess.run(["git", "-C", "/repo", "ls-files", "--others", "-i", "--exclude-standard"],
                       capture_output=True, text=True, timeout=60)
    ignored = set(r.stdout.splitlines())
except Exception as e:
    print("git ignored failed:", e)

rows = []
for root, dirs, files in os.walk(REPO):
    if ".git" in Path(root).parts:
        continue
    # skip scan output dir itself to avoid self-inclusion feedback
    for f in files:
        p = Path(root) / f
        rel = str(p.relative_to(REPO)).replace(os.sep, "/")
        if rel.startswith("experiments/audit_fixes/replay/project_cleanup_scan/"):
            continue
        try:
            st = p.stat()
            h = hashlib.sha256()
            with open(p, "rb") as fh:
                for chunk in iter(lambda: fh.read(4 * 1024 * 1024), b""):
                    h.update(chunk)
            rows.append({
                "path": rel, "size": st.st_size, "ext": p.suffix.lower(),
                "mtime": st.st_mtime, "sha256": h.hexdigest(),
                "tracked": "yes" if rel in tracked else "no",
                "ignored": "yes" if rel in ignored else "no",
                "executable": "yes" if os.access(p, os.X_OK) and not rel.endswith((".py", ".md", ".json", ".tex", ".txt", ".csv", ".yaml", ".yml", ".toml", ".pdf", ".png")) else "no",
            })
        except Exception as e:
            rows.append({"path": rel, "size": -1, "ext": p.suffix.lower(), "mtime": 0,
                         "sha256": f"ERROR:{e}", "tracked": "", "ignored": "", "executable": ""})

rows.sort(key=lambda r: r["path"])
with open(OUT / "01_full_inventory.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["path", "size", "ext", "mtime", "sha256", "tracked", "ignored", "executable"])
    w.writeheader()
    w.writerows(rows)
print(f"files: {len(rows)}, bytes: {sum(r['size'] for r in rows if r['size'] > 0)}")

# exact duplicates
byhash = {}
for r in rows:
    if r["size"] and r["size"] > 0 and not r["sha256"].startswith("ERROR"):
        byhash.setdefault(r["sha256"], []).append(r)
dups = {h: v for h, v in byhash.items() if len(v) > 1}
with open(OUT / "_dup_groups.json", "w", encoding="utf-8") as fh:
    json.dump([{"sha256": h, "size": v[0]["size"], "paths": [x["path"] for x in v],
                "tracked": [x["path"] for x in v if x["tracked"] == "yes"]} for h, v in sorted(dups.items())],
              fh, indent=1)
print(f"dup groups: {len(dups)}")

# large files
big = sorted([r for r in rows if r["size"] > 0], key=lambda r: -r["size"])[:50]
with open(OUT / "_large.json", "w", encoding="utf-8") as fh:
    json.dump([{"path": r["path"], "size": r["size"], "tracked": r["tracked"]} for r in big], fh, indent=1)
print("large top:", big[0]["path"], big[0]["size"])

# json validity
bad = []
for r in rows:
    if r["ext"] == ".json" and 0 < r["size"] < 50_000_000:
        try:
            json.load(open(REPO / r["path"], encoding="utf-8"))
        except Exception as e:
            bad.append({"path": r["path"], "size": r["size"], "error": str(e)[:120]})
with open(OUT / "_badjson.json", "w", encoding="utf-8") as fh:
    json.dump(bad, fh, indent=1)
print(f"bad json: {len(bad)}")

# empty files
empty = [r["path"] for r in rows if r["size"] == 0]
with open(OUT / "_empty.json", "w", encoding="utf-8") as fh:
    json.dump(empty, fh, indent=1)
print(f"empty: {len(empty)}")
