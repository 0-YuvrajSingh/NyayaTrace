# Temporal Eligibility Erratum

## a) Spec Text Verbatim
**From Operational Definitions table:**
| Term | Operational definition |
| --- | --- |
| Temporal existence | An authority/document is available in the corpus at or before the relevant historical time. |
| Temporal effectiveness | A statute/provision is treated as effective only during its defined validity interval when reliable metadata is available. |
| Temporal applicability | Whether the frozen historical-eligibility rule (Eligible(e,t)) permits the item for the evaluation case. |
| Provenance validity | The final citation maps to an identified source document and exact passage that was retrieved for the case/query. This is the same quantity already named “Citation Provenance Validity” in the Evaluation Metrics table below. |
| Authority consistency | The cited authority matches the predefined reference evidence/authority mapping used for evaluation. This is the same quantity already measured by “Authority-consistent Precision/Recall/F1” below. |

**From Temporal Integrity Protocol:**
Precedent eligibility should require decision_date <= case_date, with the target case and duplicates/near-duplicates excluded.
Unresolved temporal metadata must follow a predefined rule and must not be manually corrected after observing test results.

## b) Code Rule Quoted (src/legal_xai/temporal.py)
40:     if isinstance(value, bool):
41:         return None
42:     if isinstance(value, int):
43:         return value if 1 <= value <= 9999 else None
44:     if isinstance(value, (date, datetime)):
45:         return value.year
46:     if isinstance(value, str):
47:         stripped = value.strip()
48:         if len(stripped) >= 4 and stripped[:4].isdigit():
49:             return int(stripped[:4])
50:         day_month_year = re.fullmatch(r"\d{1,2}[-/]\d{1,2}[-/](\d{4})", stripped)
51:         if day_month_year:
52:             return int(day_month_year.group(1))
53:     return None
54: 
55: 
56: def assess_temporal_eligibility(
57:     ildc_query_year: int | str | None,
58:     precedent_decision_date: date | datetime | str | None,
59: ) -> TemporalDecision:
60:     """Evaluate an eCourts precedent against an ILDC case with only year metadata.
61: 
62:     ILDC's case date is available only at year granularity. To avoid temporal
63:     leakage, a precedent is eligible only when its decision year is strictly
64:     earlier. Same-year records are explicitly retained as ambiguous but excluded
65:     by default. Missing or unparseable temporal metadata is excluded.
66:     """
67: 
68:     query_year = _parse_year(ildc_query_year)
69:     precedent_year = _parse_year(precedent_decision_date)
70: 
71:     if query_year is None or precedent_year is None:
72:         return TemporalDecision(
73:             status=TemporalStatus.EXCLUDED_MISSING_METADATA,
74:             query_year=query_year,
75:             precedent_year=precedent_year,
76:             reason="ILDC query year or precedent decision date is missing or unparseable.",
77:         )
78:     if precedent_year < query_year:
79:         return TemporalDecision(
80:             status=TemporalStatus.ELIGIBLE,
81:             query_year=query_year,
82:             precedent_year=precedent_year,
83:             reason="Precedent year is strictly earlier than the ILDC query year.",
84:         )
85:     if precedent_year == query_year:
86:         return TemporalDecision(
87:             status=TemporalStatus.AMBIGUOUS_EXCLUDED,
88:             query_year=query_year,
89:             precedent_year=precedent_year,
90:             reason="Same-year ordering is unknown because ILDC provides no exact decision date.",
91:         )
92:     return TemporalDecision(
93:         status=TemporalStatus.INELIGIBLE,
94:         query_year=query_year,
95:         precedent_year=precedent_year,
96:         reason="Precedent year is later than the ILDC query year.",
97:     )
98: 
99: 
100: def partition_evidence_candidates(
101:     ildc_query_year: int | str | None,
102:     candidates: Iterable[Mapping[str, Any]],
103: ) -> TemporalCandidateBuckets:
104:     """Partition retrieved evidence using each candidate's exact decision date.
105: 
106:     The caller should return only ``eligible`` candidates to the evidence
107:     generator. The other buckets are intentionally retained for auditing,
108:     especially the same-year ambiguity bucket.
109:     """
110: 

## c) Deviation
- **Spec Rule:** `decision_date <= case_date`
- **Implemented Code Rule:** `decision_year < query_year`
Same-year authorities are admitted by the spec and excluded by the code. Missing/unparseable dates are excluded, which satisfies the spec's "predefined rule" requirement for unresolved temporal metadata. The code is stricter and cannot admit a later authority.

## d) Reason
ILDC provides only the year of each query case. Computing exact dates would require manual primary-source lookup for every query case, which exceeds the metadata provided by the benchmark.

## e) Governance Basis
The substitution of `decision_year < query_year` for the spec's `decision_date <= case_date` is an implementation-level operationalization required by ILDC's year-only metadata, documented as a deviation. The project's Scope Freeze and Change Control section is cited only for the documentation requirement: "Any such change must be documented in the reproducibility record." Thus, this erratum must be added to the reproducibility freeze record.

## f) Consequences
- Cannot admit a later authority.
- May discard eligible same-year authorities.

## g) Timing Evidence
**(i) The year-level rule existence before pre-ranking:**
- `artifacts/week4_readiness.md`
  - Line 14-15: "The smoke and QA runs logged 98 same-year candidates as `ambiguous_excluded`; none was returned as usable evidence."
  - Line 17-18: "One elephant-corridor query correctly produced no usable evidence because its highest matches were same-year." (This shows a case lost its best matches precisely due to the same-year exclusion).
- `artifacts/week9_citation_verification.md`
  - Line 11: "5. The authority decision year is strictly earlier than the ILDC query year. Same-year and later authorities fail, rather than being silently ignored."
  
**(ii) Moving the filter inside the BM25 query:**
- `artifacts/week11_temporal_preranking_investigation.md`
  - Line 5: `The existing strict temporal rule was retained without modification: an eCourts authority is eligible only when its exact decision year is strictly earlier than the ILDC query year. The sole intervention was to apply that predicate in the SQLite FTS candidate relation before ORDER BY bm25(...) LIMIT 100.`

## h) Effect on the Answer Key
Results from `experiments/audit_fixes/answer_key_temporal_check_output.txt`:
- `answer_key/authority_answer_key.json` (30 evaluation entries): 0 same-year authorities.
- `answer_key/extension_v6/verified_7_case_extension.json` (7 evaluation entries): 0 same-year authorities.

These answer-key entries were verified against the strict rule at construction. Specifically, the base 30 entries all have `temporal_status: "eligible_by_year"`, and the 7 extension entries all have `temporal_gate: "PASS"` and `temporal_eligible: True`. Therefore, the "0 same-year" result shows that no key authority was lost to the exclusion rule, not that same-year authorities are inherently irrelevant.

## i) Scripts and Output Files Used
- `experiments/audit_fixes/scripts/extract_spec.py`: Extracted paragraphs and tables from the Word document.
- `experiments/audit_fixes/spec_full_text.txt`: The raw extracted text from the Word document.
- `experiments/audit_fixes/scripts/write_quotes.py`: Extracted exact quotes and sections matching keywords from the extracted text.
- `experiments/audit_fixes/spec_temporal_quotes.md`: Markdown file containing verbatim quotes and origins from the spec.
- `experiments/audit_fixes/scripts/answer_key_temporal_check.py`: Parsed the answer key and extension files to compute entry counts and temporal classifications.
- `experiments/audit_fixes/answer_key_temporal_check_output.txt`: Raw output showing 0 same-year entries across the 37 evaluated cases.
- `experiments/audit_fixes/scripts/generate_manifest.py`: Script to generate the manifest for the directory.
- `experiments/audit_fixes/audit_fixes_manifest.json`: Manifest of all generated files.
