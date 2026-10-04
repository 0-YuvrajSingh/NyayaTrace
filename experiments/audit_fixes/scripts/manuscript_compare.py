"""Manuscript pairwise comparison (read-only)."""
import difflib
import re

R = "/repo/"
files = ["paper_master.tex", "paper_master_revised.tex", "paper_master_final.tex", "paper_master_6page.tex"]
txt = {}
for f in files:
    try:
        txt[f] = open(R + f, encoding="utf-8").read()
    except Exception as e:
        txt[f] = None
        print(f, "MISSING", e)

names = [f for f in files if txt[f]]
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        a, b = txt[names[i]].splitlines(), txt[names[j]].splitlines()
        print(f"{names[i]} vs {names[j]}: similarity={round(difflib.SequenceMatcher(None, a, b, autojunk=False).ratio(), 4)} lines={len(a)}/{len(b)}")

# section inventory per variant
for f in names:
    secs = re.findall(r"\\section\{([^}]*)\}", txt[f]) + re.findall(r"\\section\*\{([^}]*)\}", txt[f])
    print(f, "sections:", secs)

# unsupported-claim markers per variant
markers = {
    "combined central (185/185)": "185/185",
    "LLM 56/56": "56/56",
    "positive controls 37/37": "37/37",
    "typescript compile": "TypeScript compile",
    "four cases retrieved+selected (1985_40 bug)": "four cases (",
    "29 byte-exact": "29 byte-exact",
    "combined E3/E4 0.648649": "0.648649",
    "12/37": "12/37",
    "byte-identical E3/E4": "byte-identical E3",
    "no leakage whatsoever": "no leakage whatsoever",
    "guarantee that no displayed": "guarantee that no displayed",
    "IEEEtrigger": "IEEEtrigger",
}
for name, mk in markers.items():
    print(name, {f: (txt[f].count(mk) if txt[f] else "NA") for f in files})
