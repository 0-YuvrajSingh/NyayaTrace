"""Count cleaned chunk lines per year for the two IDs (read-only)."""
import glob
import json

n = {}
for f in sorted(glob.glob("/repo/corpus/ecourts/cleaned/year=*/chunks.jsonl")):
    year = f.split("year=")[1][:4]
    c292 = c293 = 0
    with open(f, encoding="utf-8") as fh:
        for line in fh:
            if "1980_2_292_297" in line:
                c292 += 1
            if "1980_2_293_297" in line:
                c293 += 1
    if c292 or c293:
        n[year] = (c292, c293)
print("cleaned (292,293) per year:", n)
