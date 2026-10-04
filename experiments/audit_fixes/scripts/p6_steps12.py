import json
import re
from pathlib import Path
import sys

def get_freeze_info():
    print("--- 1. COUNT RECONCILIATION ---")
    with open('/repo/config/reproducibility_freeze.json', 'r', encoding='utf-8') as f:
        freeze_data = json.load(f)
    
    def extract_paths(obj, current_path=""):
        paths = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == "sha256":
                    paths.append({"file": obj.get("file", ""), "sha256": v, "parent": current_path})
                else:
                    paths.extend(extract_paths(v, current_path + "." + k if current_path else k))
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                paths.extend(extract_paths(item, current_path + f"[{i}]"))
        return paths
    
    entries = extract_paths(freeze_data)
    total_hashes = len(entries)
    
    path_map = {}
    for e in entries:
        path_map.setdefault(e["file"], []).append(e)
    
    unique_paths = len(path_map)
    duplicates = {k: v for k, v in path_map.items() if len(v) > 1}
    
    print(f"freeze_entries = {total_hashes}")
    print(f"unique_freeze_paths = {unique_paths}")
    print(f"duplicate_occurrences = {len(duplicates)}")
    for k, v in duplicates.items():
        print(f"  Duplicate: {k}")
        for occ in v:
            print(f"    Parent: {occ['parent']}, Hash: {occ['sha256']}")
            
    # hash_table.md rows
    with open('/repo/experiments/audit_fixes/hash_table.md', 'r', encoding='utf-16') as f:
        lines = [l.strip() for l in f if l.strip().startswith('|')]
    data_lines = [l for l in lines if not l.startswith('| Path') and not l.startswith('|---')]
    print(f"hash_table_rows = {len(data_lines)}")
    for l in data_lines:
        print(f"  {l.split('|')[1].strip()}")
        
    # docs/freeze_drift_audit.md rows
    with open('/repo/docs/freeze_drift_audit.md', 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f if l.strip().startswith('|')]
    data_lines_audit = [l for l in lines if not 'File Path' in l and not l.startswith('|---')]
    print(f"freeze_drift_audit_rows = {len(data_lines_audit)}")
    for l in data_lines_audit:
        parts = l.split('|')
        if len(parts) > 2:
            print(f"  {parts[2].strip()}")

def get_answer_key_info():
    print("\n--- 2. ANSWER-KEY CASE COUNT ---")
    with open('/repo/artifacts/answer_key_reresolution.md', 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f if l.strip().startswith('|')]
    
    flagged = []
    for l in lines:
        if 'New:' in l or 'Corrected:' in l or 'Replaced' in l or 'corrected' in l.lower():
            if not 'File Path' in l and not l.startswith('|---'):
                flagged.append(l)
    
    print(f"Total flagged cases in answer_key_reresolution.md: {len(flagged)}")
    flagged_ids = set()
    for row in flagged:
        print(row)
        # Extract things like 2013_35, 2013_30, etc.
        matches = re.findall(r'\b(19\d\d_\d+|20\d\d_\d+)\b', row)
        for m in matches:
            flagged_ids.add(m)
            
    print("\nOccurrences in week12_prediction_cross_reference.json:")
    with open('/repo/artifacts/week12_prediction_cross_reference.json', 'r', encoding='utf-8') as f:
        w12 = json.load(f)
    
    def search_id(obj, current_path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if any(fid in k for fid in flagged_ids):
                    print(f"Found key match at: {current_path}.{k}")
                search_id(v, current_path + "." + k if current_path else k)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                if isinstance(item, str) and any(fid in item for fid in flagged_ids):
                    print(f"Found value match at: {current_path}[{i}] = {item}")
                search_id(item, current_path + f"[{i}]")
        elif isinstance(obj, str):
            if any(fid in obj for fid in flagged_ids):
                print(f"Found string match at: {current_path} = {obj}")

    search_id(w12)

get_freeze_info()
get_answer_key_info()
