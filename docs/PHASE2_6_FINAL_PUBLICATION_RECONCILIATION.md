# Phase 2.6 — Final publication reconciliation audit

## 1. Repository commit before changes

HEAD `02bf753` ("Final submission alignment, artifact regeneration, and
repository audit"); prior `d88c0bf`, `2bd02b3`. Tree was clean at audit
start. No paper_master.tex exists anywhere in the repo (glob `**/*.tex` =
zero files); none was supplied. Phases D–G are therefore BLOCKED (see §14).

## 2. Integrity fix performed

NONE required. The reported extension-manifest hash conflict does NOT
reproduce: manifest-recorded vs actual SHA-256 match exactly for both
`verified_7_case_extension.json` (`afa0329f…4495d`) and
`verification_results.json` (`8939dba5…2016a1d`). The three files were
committed together in `d88c0bf`, and all 7 extension passage IDs/texts and
all 7 statuses match the current verification records (v2/v3 upgrades
included). Likely cause of the earlier finding: hash computed over a
different serialization or a mid-workflow state. Per A6 (never mutate
frozen content to match an old hash) and the absence of any discrepancy,
no correction was made and no integrity commit was created.

## 3. Old/new hashes

Old recorded = actual = authoritative (no change):
- extension: `afa0329f49afc7041cc824bcbee0e4469097588b03bc3f9009b547bb2ff4495d`
- verification-results: `8939dba56b714449bfe540ce7c50f949bb9b2282ab9355a1b27633a12016a1d9`
- base 30-case key: `f4ccb0fa…00e81` (matched; untouched).
Tests run: host suite 75 passed (torch pair environment-limited, green
in-container previously). Final status: internally consistent; nothing to fix.

## 4. Tests run and results

`pytest tests/`: 75 passed, 0 failed (host subset; E2/torch files require
the E2 image by design). No test relates to the manifest hashes; integrity
was verified by direct SHA-256 recomputation instead.

## 5–7. Authoritative populations and metrics (re-read from JSON, not prompt)

- RQ1: base30 R@5 12/30=0.40, R@100 15/30=0.50, 150 citations, E3/E4
  0.666667/0.603175 CM [[4,3],[7,16]]; ext7 R@5 0/7, R@100 5/7=0.714286,
  35 citations, E3/E4 0.571429/0.571429 CM [[2,0],[3,2]]; combined37 R@5
  12/37=0.324324, R@100 20/37=0.540541, 185 citations, E3 0.648649/0.607347
  CM [[6,3],[10,18]].
- RQ2 combined37: groundedness 37/37, provenance 185/185, temporal 0/185,
  unsupported 0/37, rejections 0; probes 37/37 × 3 mutation types.
- RQ3: 14 cases × 4 LLM evaluators (Gemini, Claude Sonnet 4.6, DeepSeek,
  GPT-5.6 Luna), 112 display ratings, 56 forced preferences (structured
  56/56), 5 dimensions (linkage +1.75, verifiability +1.0, traceability
  +2.482143, clarity +2.517857, transparency +1.982143; overall +1.946429).
- E1 (N=1503): 0.61344/0.612342 CM [[501,248],[333,421]]. E2 mean-logit:
  0.596806/0.592358 CM [[527,222],[384,370]].
- RQ3 reconciliation: 14-case LLM study is the principal RQ3 result (noted
  exploratory, non-human, identical DeepSeek/GPT outputs disclosed and
  retained separately); n=7 self-review retained only as formative,
  labeled `author_self_review_fallback`, never human evidence.

## 8. Manuscript-section → artifact mapping (for the pending .tex pass)

Abstract→RQ1-combined37 + RQ2-185/185 + RQ3-56/56-exploratory; Problem→
secondary-prediction framing; Data→30+7+37 with strata rationale;
RQ1→§6 values; RQ2→probe triplet + ceiling disclosure; RQ3→dimension
table + unanimity + anomaly note; Tables→Base-30/Extension-7/Combined-37
labels, 150/185 never conflated, unsupported den=37; Figures→(a) regenerate
outcome/retrieval bars to 37-state, (b) keep frozen-30 figures only with
base captions, (c) new RQ3 dimension chart from §7 JSON; Limitations→§9
list below; Conclusion→bounded wording only.

## 9. Figure/table reconciliation

Pending manuscript availability. Authoritative plotting sources:
`artifacts/e1_e2_comparison.json`, `experiments/rq1/rq1_results.json`
(strata), `experiments/rq2/rq2_results.json`, `experiments/rq3/
rq3_results.json`, `answer_key/extension_v6/extension_manifest.json`.
No decorative figures permitted.

## 10. Citation verification status

- Pooja Ramesh Singh (2026 INSC 668): present in `submission/paper.md:357`
  biblio with URL; content consistent with repo usage. Live URL
  verification NOT performed in this audit — flagged, not fabricated.
- `casefacts2026`, `taxflow2026`: ZERO occurrences anywhere in the repo;
  they cannot be verified from repository content. If the external
  manuscript cites them, their publication details are UNVERIFIED and must
  be confirmed or removed before submission.

## 11. Remaining UNVERIFIED items

Manuscript-dependent checks (D–G) unexecuted for lack of the .tex file;
live-URL checks for bibliography entries; visual PDF inspection of a
not-yet-existing build.

## 12. Remaining limitations (must survive into the manuscript)

N=37 descriptive; additive extension postdates the freeze; single-authority
reference; year-granular temporal rule; provenance≠correctness; prediction≠
correctness; RQ3 non-human/exploratory + evaluator-identity anomaly;
bundled E4; English/SCI/ILDC scope; semester prototype; no production claim.

## 13. Publication-blocking discrepancies in scope

None found in repository artifacts. The sole blocker is procedural: no
`paper_master.tex` exists to revise, so manuscript reconciliation,
figure/table rebuilds, bibliography hardening in .tex, and PDF
compilation/visual inspection could not be performed.

## 14. Final verdict: BLOCKED

Blocked solely by the missing manuscript file (`paper_master.tex`
absent from the repo and not otherwise supplied). All repository-side
preconditions for the manuscript pass are met: integrity holds with no
correction needed, authoritative values are mapped above, RQ3 is
reconciled, citations are triaged, and the audit trail is complete.
Nothing was committed (no change existed to commit); nothing pushed.
Supply the .tex file (or point to its location) to unblock Phases D–G.
