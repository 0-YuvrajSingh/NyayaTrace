import json
data = json.load(open('/repo/artifacts/answer_key_alignment_audit.json'))
for r in data['rows']:
    if 'fail' in r['status']:
        print(f"{r['query_case_id']} - {r['status']}")
