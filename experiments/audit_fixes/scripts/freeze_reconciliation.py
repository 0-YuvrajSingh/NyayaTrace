import json, os, glob
from collections import Counter

def main():
    freeze_files = glob.glob('/repo/**/freeze_*.json', recursive=True)
    counts = {}
    for f in freeze_files:
        try:
            with open(f) as fp:
                data = json.load(fp)
            if isinstance(data, dict) and 'items' in data:
                c = Counter(item.get('status', 'unknown') for item in data['items'])
                counts[os.path.basename(f)] = dict(c)
        except Exception:
            pass
    print("Entries per status in every freeze file:")
    print(json.dumps(counts, indent=2))
    
    # Also get the eCourts corpus count
    corpus_count = 0
    import jsonlines
    ecourts_files = glob.glob('/repo/corpus/ecourts/cleaned/**/*.jsonl', recursive=True)
    for f in ecourts_files:
        with jsonlines.open(f) as reader:
            for _ in reader:
                corpus_count += 1
    print(f"\neCourts actual corpus count: {corpus_count}")
    
    with open('/repo/experiments/audit_fixes/FREEZE_RECONCILIATION.md', 'w') as out:
        out.write("# Freeze Manifest Reconciliation\n\n")
        out.write("## Status Counts in Freeze Files\n")
        for f, c in counts.items():
            out.write(f"- **{f}**:\n")
            for status, count in c.items():
                out.write(f"  - {status}: {count}\n")
        
        expected = 2343435
        out.write(f"\n## Corpus Count Reconciliation\n")
        out.write(f"- Expected eCourts corpus records: {expected}\n")
        out.write(f"- Actual eCourts corpus records (computed from JSONL): {corpus_count}\n")
        if expected == corpus_count:
            out.write("- Discrepancy: None.\n")
        else:
            out.write(f"- Discrepancy: {corpus_count - expected}\n")

if __name__ == '__main__':
    main()
