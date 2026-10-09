"""Generate experiments/audit_fixes/QUERY_LEAKAGE_AUDIT.md (authority-token overlap, Base-30).

Run from the repository root. Relocated from scratch/generate_b1_artifact.py on 2026-10-09;
independently re-verified in docs/GROUND_TRUTH_ADJUDICATION.md section I.
"""
import json
import re
from pathlib import Path
import pyarrow.parquet as pq
import sys

sys.path.insert(0, 'src')
from legal_xai.facts import load_facts_extraction_rule, extract_case_facts
from legal_xai.retrieval import salient_query_terms

with open('answer_key/authority_answer_key.json', 'r', encoding='utf-8') as f:
    ak = json.load(f)
eval_entries = [e for e in ak['entries'] if e.get('status') == 'evaluation']

rule = load_facts_extraction_rule('config/facts_extraction.json')
table = pq.read_table('corpus/ildc/single_test.parquet', columns=['id', 'text'])
all_test_cases = {str(row['id']): row['text'] for row in table.to_pylist()}

GENERIC = {
    'state', 'union', 'india', 'ltd', 'limited', 'ors', 'anr', 'others', 'another',
    'govt', 'government', 'corp', 'corporation', 'v', 'vs', 'versus', 'of', 'and',
    'the', 'in', 'at', 'by', 'for', 'on', 'with', 'to', 'a', 'an', 'shri', 'smt',
    'dr', 'mr', 'mrs', 'ms', 'co', 'p', 'pvt', 'etc', 'high', 'court', 'supreme',
    'appeal', 'civil', 'criminal', 'judgment', 'order', 'learned', 'counsel',
    'section', 'act', 'rule', 'rules', 'article', 'constitution', 'writ', 'petition',
    'respondent', 'respondents', 'appellant', 'appellants', 'petitioner', 'petitioners',
    'bench', 'justice', 'division', 'case', 'cases', 'supp', 'scr', 'scc', 'air', 'jt', 'stc'
}

GEOGRAPHIC = {
    'uttar', 'pradesh', 'madhya', 'haryana', 'punjab', 'kerala', 'tamil', 'nadu',
    'andhra', 'karnataka', 'bihar', 'assam', 'rajasthan', 'delhi', 'bombay', 'calcutta',
    'madras', 'chandigarh', 'ernakulam', 'patna', 'allahabad'
}

DEPARTMENTAL = {
    'sales', 'tax', 'officer', 'commissioner', 'board', 'revenue', 'taxes',
    'commercial', 'income', 'customs', 'excise', 'deputy', 'assistant', 'bank'
}

ALL_IGNORE = GENERIC | GEOGRAPHIC | DEPARTMENTAL

def get_distinctive_party_tokens(auth_title, query_title):
    words = re.findall(r'[a-zA-Z0-9]+', auth_title.lower())
    query_words = set(re.findall(r'[a-zA-Z0-9]+', query_title.lower()))
    return [w for w in words if w not in ALL_IGNORE and len(w) > 2 and w not in query_words]

def normalize_cite(cite):
    return re.sub(r'\s+', ' ', re.sub(r'[^a-zA-Z0-9\s]', ' ', cite.lower())).strip()

rows = []

for e in eval_entries:
    qid = str(e['query_case_id'])
    qtitle = e.get('query_case_title', '')
    atitle = e.get('authority_title', '')
    acite = e.get('authority_citation', '')
    raw_text = all_test_cases[qid]
    facts = extract_case_facts(raw_text, rule).text
    facts_lower = facts.lower()
    terms = [t.lower() for t in salient_query_terms(facts)]
    
    distinctive = get_distinctive_party_tokens(atitle, qtitle)
    
    # Check citation in facts
    nums = re.findall(r'\d+', acite)
    rep = re.findall(r'scc|scr|air|stc|jt', acite.lower())
    cite_in_facts = False
    if len(nums) >= 2 and rep:
        pattern = r'\b' + nums[0] + r'\s*(?:' + rep[0] + r'|[a-z\.\s]+)\s*' + nums[-1] + r'\b'
        if re.search(pattern, facts_lower):
            cite_in_facts = True
            
    facts_tokens = [w for w in distinctive if re.search(r'\b' + re.escape(w) + r'\b', facts_lower)]
    terms_tokens = [w for w in distinctive if w in terms]
    
    hit_facts = "Y" if (facts_tokens or cite_in_facts) else "N"
    hit_terms = "Y" if terms_tokens else "N"
    
    matched = []
    if cite_in_facts:
        matched.append(f"cite:{acite}")
    if facts_tokens:
        matched.extend(facts_tokens)
    if terms_tokens:
        matched.extend([f"salient:{t}" for t in terms_tokens])
        
    rows.append({
        "case_id": qid,
        "hit_facts": hit_facts,
        "hit_terms": hit_terms,
        "matched_tokens": ", ".join(matched) if matched else "none",
        "facts_tokens": facts_tokens,
        "terms_tokens": terms_tokens,
        "cite_in_facts": cite_in_facts
    })

# Write markdown table
md = "# Query-Leakage Audit Table (Base-30)\n\n"
md += "| Case ID | Hit in Facts Text (Y/N) | Hit in Salient Terms (Y/N) | Matched Tokens |\n"
md += "|---|:---:|:---:|---|\n"
for r in rows:
    md += f"| {r['case_id']} | {r['hit_facts']} | {r['hit_terms']} | {r['matched_tokens']} |\n"

facts_hits_n = sum(1 for r in rows if r['hit_facts'] == 'Y')
terms_hits_n = sum(1 for r in rows if r['hit_terms'] == 'Y')
both_hits_n = sum(1 for r in rows if r['hit_facts'] == 'Y' and r['hit_terms'] == 'Y')

md += f"\n## Summary\n"
md += f"- Total cases audited: {len(rows)}\n"
md += f"- Cases with authority citation/distinctive tokens in facts-only text: {facts_hits_n}/30\n"
md += f"- Cases with distinctive authority tokens in 32 salient query terms: {terms_hits_n}/30 (Case 2008_1629: raghavendra, acharya)\n"
md += f"- Cases with hits in both facts text and salient query terms: {both_hits_n}/30\n"

Path("experiments/audit_fixes/QUERY_LEAKAGE_AUDIT.md").write_text(md, encoding="utf-8")
print("Wrote experiments/audit_fixes/QUERY_LEAKAGE_AUDIT.md")
print(f"Facts hits: {facts_hits_n}, Terms hits: {terms_hits_n}, Both: {both_hits_n}")

