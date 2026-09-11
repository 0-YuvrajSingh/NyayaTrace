# RQ3 design audit — structured explanation vs control (read from implementation)

## 1. Structured explanation format (frozen E4 renderer)

`src/legal_xai/grounded_answer.py::render_grounded_answer` (renderer
`week10-verified-explanation-renderer-v1`, extract-only): five fixed
sections — legal_issue; applicable_law_and_cases (authority list);
supporting_evidence (verbatim passages); conclusion (frozen
non-inferential boilerplate); uncertainty (fixed research-brief
disclaimer + insufficiency signaling when evidence is thin).

## 2. Field constitution

- Issue: `legal_issue` (query context excerpt, no new legal claims).
- Authority/Rule: `applicable_law_and_cases[]` — one item per selected
  evidence: evidence_id, case_id, citation, decision_date, court.
- Evidence: `supporting_evidence[]` — evidence_id, chunk_id, verbatim
  passage + full provenance (source_id, pdf/page/char locators).
- Conclusion: frozen boilerplate tied only to displayed evidence IDs;
  `assert_answer_grounded` rejects any inferential conclusion.

## 3. Evidence↔section linkage

Explicit and mechanical: every authority item carries the evidence_id of
its verbatim passage; every passage carries chunk_id + provenance. The
assertion gate fails the answer if any link is altered or unlinked.

## 4. Displayed citation/provenance metadata

Per item: reporter citation, decision date, court, source_id, page,
citation (chunk) ID. No hidden provenance: everything displayed is
verifiable against `corpus_chunks` + `retrieval_results`.

## 5. Uncertainty/limitations

Fixed uncertainty text (research brief, not advice; reports only selected
passages) + evidence_sufficiency (0→insufficient, 1→limited, ≥2→multiple)
+ explicit insufficiency statement when nothing eligible is selected.

## 6. Non-structured presentation in-repo

Legitimate and pre-existing: `render_unstructured` in
`scripts/build_week13_rq3_review_packet.py:65-78` renders the IDENTICAL
evidence set (same chunk IDs, enforced by parity check, script lines
163-167) as a flat citation+text list without the Issue→Authority→
Evidence→Conclusion order. It is a presentation transform, not a
re-retrieval or rewrite.

## 7. Control validity

VALID. A = unstructured presentation, B = structured evidence-linked
explanation, both generated from the same frozen verified evidence sets
with citation-ID parity enforced. No invention, no post-hoc structure
stripping, no output rewriting. Frozen A/B packet exists for 7 base-30
cases: `artifacts/week13_review_packet.md` + parity audit
`artifacts/week13_rq3_ablation_parity.json` (7/7 parity).

## 8. Existing independent human-evaluation mechanism

ABSENT. The only completed ratings (`week13_review_response_completed.json`,
2026-09-03) are `author_self_review_fallback` with `outside_reviewer:
false`. Template + packet + parity machinery exist; independent raters do
not. Automated verifier checks and any LLM judgment are explicitly NOT
human evaluation and are not used as such here.

## 9. Packet generation without touching frozen artifacts

YES for base-7 (frozen packet already exists; evaluate as-is). For ext7,
packets are renderable on demand from RQ1's actual selected evidence +
corpus verbatim text with the same frozen render functions and parity
rule; rendering is deterministic presentation, not a model/output change.
No frozen file needs modification in either path.
