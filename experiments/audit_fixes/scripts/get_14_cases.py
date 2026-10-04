import json, pyarrow.parquet as pq
from legal_xai.facts import extract_case_facts, facts_input_is_eligible, load_facts_extraction_rule

config = json.loads(open('/repo/config/e1_baseline.json').read())
rule = load_facts_extraction_rule(config["facts_extraction_config"])

table = pq.read_table('/repo/' + config["fixed_split_files"]["test"], columns=["id", "text"])
excluded_ids = []
for row in table.to_pylist():
    result = extract_case_facts(row["text"], rule)
    if not facts_input_is_eligible(result, rule):
        excluded_ids.append(row["id"])

print("The 14 excluded case IDs:", excluded_ids)

answer_key = json.load(open('/repo/answer_key/authority_answer_key.json'))
ak_ids = [entry['query_case_id'] for entry in answer_key]
overlap = set(excluded_ids) & set(ak_ids)
print("Excluded IDs in answer key:", overlap if overlap else "None")
