# Cleanup delta report (G1-G4)

1. File count: 42469 -> 39922 (delta -2547)
2. Total bytes: 31370667970 -> 31255227874 (delta -115440096)
3. Directory count: 546 -> 293 (delta -253)
4. Exact dup groups: 5320 -> 5226 (delta -94)
5. Near-duplicates: recheck below (paper variants + script pairs intact expected)
6. Generated/temp: before ext {'.pdf': 39088, '.js': 1430, '.map': 412, '.json': 277, '.ts': 217, '.md': 207, '.py': 159, '.log': 106}
   after ext {'.pdf': 39088, '.json': 171, '.py': 163, '.md': 132, '.parquet': 74, '.jsonl': 71, '.log': 38, '.npy': 30}
11. Added files (4):
    + experiments/audit_fixes/scripts/cleanup_delta.py
    + experiments/audit_fixes/scripts/cleanup_join.py
    + experiments/audit_fixes/scripts/cleanup_rescan.py
    + experiments/audit_fixes/scripts/cleanup_stats.py
12. Removed files (2551): expected G1+G2+G3+G4 only
    unexpected removals: NONE
