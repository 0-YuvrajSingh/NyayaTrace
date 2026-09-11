# Scope-conformance audit — repository vs canonical spec (Indian_Legal_XAI.docx, Document 3 Final)

READ-ONLY. No implementation, experiment, dataset, artifact, or paper file
changed. Every status grounded in inspected code/artifacts, not filenames.
Statuses: IMPLEMENTED / IMPLEMENTED WITH DOCUMENTED LIMITATION /
OPTIONAL-FEASIBILITY NOT IMPLEMENTED / DEFERRED / OUT OF SCOPE-CORRECTLY
ABSENT / NOT IMPLEMENTED-SCOPE GAP / CONFLICTS WITH SCOPE.

## 1. Executive verdict: CONFORMANT WITH DOCUMENTED LIMITATIONS

Core research scope conforms: explainable decision-support (not autonomous),
Indian Supreme Court corpus, English core, BM25 retrieval, evidence
selection, provenance, citation verification, year-granular temporal gate,
structured explanation, human-review requirement, no chain-of-thought
exposure, E1–E4 present with frozen configs, reference evidence predefined
by procedure (not retrieval-derived), freeze record complete, paper +
figures + error analysis + static demo present. Three genuine deviations
(RQ labeling incl. a 4th RQ; strict-< vs <= temporal; post-freeze 37-case
reference offering) and three minor deliverable gaps (React/Spring demo,
efficiency metrics, architecture diagram) are documented below. No
GraphRAG/agents/multilingual/SaaS/leaderboard/new-model creep found.

## 2. Requirement matrix (condensed; evidence paths verified by inspection)

| # | Requirement (spec location) | Repository evidence | Status |
|---|---|---|---|
| A | Explainable decision-support identity; no autonomous judge (Exec summary, Scope table, Governance) | `README.md` scope block; `grounded_answer.py` non-inferential conclusion; demo read-only | IMPLEMENTED |
| B | Secondary: outcome prediction (Primary/Secondary table) | E1/E2/E3-E4 prediction as secondary measure; paper §11.2 | IMPLEMENTED |
| C1 | RQ1 grounding-vs-baseline (RQs) | Answered as E2-vs-E3 retrieval/prediction comparison (frozen eval + session RQ1), BUT paper labels "RQ1: E1-vs-E2 outcome baselines" | CONFLICTS (labeling; substance exists, see §RQ1) |
| C2 | RQ2 provenance/citation (RQs) | E3-vs-E4 A/D ablation + probes; `experiments/rq2/` | IMPLEMENTED |
| C3 | RQ3 structured transparency (RQs) | A/B packet + parity + exploratory LLM eval; human pending | IMPLEMENTED WITH DOCUMENTED LIMITATION |
| C4 | ONLY three RQs in scope | Paper §5 adds "RQ4 – evidence-augmented prediction" | CONFLICTS (minor, terminological) |
| D | H1/H2/H3 (Hypotheses) | Paper §5 reports all three with dispositions (H1 not supported; H2 bounded support; H3 non-independent) | IMPLEMENTED |
| E | Objectives: pipeline, grounding, provenance, temporal, structured expl., metrics, governance | `src/legal_xai/` (10 modules) + configs + freeze + paper §14 | IMPLEMENTED |
| F | Scope table: BM25 core; semantic only exploratory; controlled generation; no GraphRAG/ensembles/prod search | `retrieval/bm25.sqlite` FTS5; no dense/graph code (grep 0 hits); extract-only renderer (stricter than required) | IMPLEMENTED (exploratory semantic correctly absent) |
| F | English core; multilingual deferred | English-only corpus/code; no multilingual implementation (0 hits) | IMPLEMENTED |
| G | Non-goals: AI judge, authority claims, multilingual core, commercial search, GraphRAG/agents, leaderboard, confidence=certainty | 0 hits for all flagged families; uncertainty boilerplate; no certitude claims in reports | OUT OF SCOPE-CORRECTLY ABSENT |
| H | Output contract (11 items) | Renderer emits issue/authorities/prediction/verbatim passages/authority meta/verification status/provenance/temporal/explanation/uncertainty/human-review flag (`grounded_answer.py:115-180`; E4 answer dict) | IMPLEMENTED |
| I | Architecture: query→NLP→corpus→temporal→BM25→top-k→selection+outcome→explainability→citation check→human output | Implemented exactly (`evidence_pipeline.py` + `run_grounded_answer_pipeline.py`); explanation points only to retrieved set (assert gate) | IMPLEMENTED |
| J | Components: ILDC, Python preproc, TF-IDF+LogReg, Legal-BERT, BM25/Lucene, selection rule, controlled generation, explanation, validator, Postgres+files, demo | All present except demo stack form (see gap 3) | IMPLEMENTED (demo: see §14) |
| K | E1 TF-IDF+LogReg facts benchmark | `train_e1_baseline.py`, frozen C=10.0, reproduced exact | IMPLEMENTED |
| K | E2 Legal-BERT facts-only | InLegalBERT ckpt-6318, 512/50, mean-logit; discarded 256-prefix retained transparently | IMPLEMENTED |
| K | E3 retrieval-grounded + BM25, same splits/index/top-k/seed | `run_evidence_pipeline.py`; shared configs; RQ1 run | IMPLEMENTED |
| K | E4 = E3 + provenance selection + citation validation + structured expl + temporal | `run_grounded_answer_pipeline.py`; verifier-v2; renderer-v1; bundled caveat documented (paper §9.8) | IMPLEMENTED WITH DOCUMENTED LIMITATION (bundled, disclosed) |
| L | Temporal: decision_date <= case_date; target/dup excluded; predefined unresolved rule | Implemented STRICTER: precedent_year < query_year, same-year ambiguous-excluded (`temporal.py:78-88`); duplicates via alignment gate; deterministic; no post-hoc correction | IMPLEMENTED WITH DOCUMENTED LIMITATION (deviation conservative + disclosed §13.6) |
| L | Statute effective/end-validity intervals | Corpus is precedent-only; no statute validity metadata exists | DEFERRED (corpus-role limitation; §13.1) |
| M | Explainability: linkage rate, authority P/R/F1, rationale, attribution if feasible, Issue→Authority→Evidence→Conclusion, uncertainty, no CoT | All except model attribution (extract-only design; "where feasible" not triggered) | IMPLEMENTED (attribution: OPTIONAL-FEASIBILITY NOT IMPLEMENTED) |
| N | Citation chain final→identity→doc→passage→retrieved→temporal→valid/reject; 9 minimum fields | `citation_verifier.py:113-174` enforces chain; fields present: source_id, case_id≈authority_name, citation, chunk_id≈passage_id, rank/score, date, temporal status, query/run IDs. `source_type` absent as a field (single-type precedent corpus — cosmetic) | IMPLEMENTED WITH DOCUMENTED LIMITATION |
| N | Traceability ≠ correctness distinction | Paper §12.3 + reports repeat it; 138 nonmatches unlabeled | IMPLEMENTED |
| O | Retrieval R@5/R@k; Authority P/R/F1; groundedness; temporal violation (sole temporal metric); provenance validity; human/exploratory explanation; unsupported rate; Acc/Macro-F1 | All implemented/reported (R@5/R@100, 0.08/0.40/0.1333, 1.0, 0.0, 1.0, LLM-exploratory clearly labeled, 0.0, Acc/F1); no invented extra required metrics | IMPLEMENTED |
| O | Efficiency latency/memory/compute | No timing measurement found in code or artifacts | NOT IMPLEMENTED-SCOPE GAP (minor) |
| P | 7 mandatory error categories | Covered: E2-wrong/E3-right (2 cases); E3-right/E4-wrong (0, reported); correct-pred-unsupported (0); retrieved-but-wrong (4); traceable-not-selected (18); later-than-date (0 violations); highlights-without-evidence (0/5 spot). Paper §12 | IMPLEMENTED |
| Q | Governance: oversight, non-autonomy, citation boundary, audit logging, privacy, bias-if-supported, uncertainty, contestability | Fail-closed verifier; run persistence; uncertainty boilerplate; read-only demo; bias-subgroup n/a per conditional wording; DPDP/auth partial (local single-user; documented as deployment requirement) | IMPLEMENTED WITH DOCUMENTED LIMITATION |
| R | ILDC principal benchmark; attributable corpus with identity/dates/boundaries; no gratuitous expansion | ILDC 7,593 frozen; eCourts 39k PDFs/2.34M chunks with locators; dedup + quality audits | IMPLEMENTED |
| S | No confidential leaks to external APIs; auth/RBAC; hash assets; cache index; immutable run IDs; bounded top-k; read-only demo | Local-only execution; no API calls in pipeline (grep); hashes frozen; run UUIDs; k=100/5; allowlisted static server | IMPLEMENTED (auth/RBAC: local-scope limitation, documented) |
| T | 14-item freeze (dataset→deps) | `reproducibility_freeze.json` v4 covers all 14; verified 34/34 + clean replay | IMPLEMENTED (known mutabilities — torch tails, image tags — disclosed) |
| U | Deliverables: E1–E4, index, citation module, expl module, tables/plots, error report, freeze manifest, demo, paper, presentation/diagram | All per `submission/MANIFEST.md` EXCEPT: demo is static stdlib (not React+Spring) and no standalone architecture-diagram file (results figures only) | IMPLEMENTED except 2 minor gaps (see §14) |
| V | Paper structure (19 sections) | `submission/paper.md` covers all incl. operational definitions, bundled caveat, limitations, artifact map | IMPLEMENTED |
| W | Limitations/future work (8 + 10 items) | Paper §13 (9 categories) + future-work list incl. multilingual/hybrid/user studies | IMPLEMENTED |
| X | Scope freeze/change control | v4 IDs frozen; transfer guard; addenda (v5/v6) additive-only; RQ4-label + 37-case timing are the only unlogged deviations (flagged §§RQ1,17) | IMPLEMENTED WITH DOCUMENTED LIMITATION |

## 3. Core scope / RQ1 / RQ2 / RQ3 / E1–E4 / contract / metrics / temporal / provenance / error analysis / governance / deliverables / reproducibility / exclusions

Covered in the matrix; notes: (§4 RQ1) substance of the frozen grounding question is answered (E2-vs-E3 retrieval + evidence-augmented prediction, N=30/37) but paper §5 labels RQ1 as "E1-vs-E2 outcome baselines" — relabel to match the canonical question; (§6 RQ3) wording adds "source clarity…appropriate trust" dimensions consistent with the canonical transparency construct; human evaluation absent → (a) target = human-verifiable transparency, (b) actual = blinded LLM exploratory (56/56 structured, unanimous — reported without significance claims), (c) unestablished = any human-rated effect. (§5 RQ2) temporal correctly NOT described as E4-only: selection enforces pre-rank, verifier re-enforces; reports keep the distinction. (§7) no experiment changed definition (256-token run marked discarded, not silently replaced).

## 4. Missing but NOT scope violations

Semantic/hybrid retrieval, learned reranking, model attribution, calibration analysis, bias-subgroup measurement, statute validity intervals, production auth/RBAC/DPDP operationalization, multilingual — all explicitly optional ("where feasible"/"if feasible"/conditional) or deferred to future work in the spec.

## 5. Actual scope risks

1. (Moderate) RQ labeling drift + added RQ4: paper §5 must be reconciled to exactly three canonical RQs (fold prediction analysis under RQ1/RQ2 as secondary, per spec's own E3 wording).
2. (Moderate) 37-case reference built post-freeze: constructed mechanically (SCR mining, not retrieval output) with gates + preserved 30-case results, but postdates test evaluation — disclose timing in paper; never present as preregistered.
3. (Low) Temporal strictness (`<` vs spec `<=` with same-year exclusion): conservative, disclosed; confirm frozen wording stays consistent.
4. (Low) Statute half of retrieval scope unbuilt (precedent-only corpus): disclose as corpus-role limit.
5. (Low) Efficiency metrics absent despite metric-table listing.

## 6. Claims the final paper MUST NOT make

Legal correctness from provenance; retrieval completeness; statistical superiority/significance; human-rated effects from LLM data; production readiness; generalization beyond evaluated sets; confidence-as-certainty; causal attribution from bundled E4; multilingual capability; autonomous decision fitness. (Current reports already avoid these; keep the guardrails.)

## Verdict inputs

- `git status`: only untracked additive dirs (`answer_key/expansion_v5/`, `answer_key/extension_v6/`, `experiments/`, `validation_prep/`, `validation_replay/`); `git diff --stat`: empty (no tracked modifications).
