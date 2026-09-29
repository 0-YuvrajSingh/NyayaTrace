"""6-page compression batch 4: limitations/governance/conclusion (non-aborting)."""
from pathlib import Path

R = Path("/repo")
t = (R / "paper_master_6page.tex").read_text(encoding="utf-8")

EDITS = [
("""\\textbf{Answer-key size and era concentration.} Evidence evaluation rests on
30 frozen cases, extended additively to 37;
13 of the base 30 are from
the 1980s. The combined set is neither large nor era-balanced and should not
be read as representative of the ILDC test set or of
Indian legal research generally.""",
"""\\textbf{Answer-key size and era concentration.} Evidence rests on
30 frozen cases, extended to 37;
13 of the base 30 are from
the 1980s: neither large nor era-balanced, not
representative of Indian legal research generally."""),
("""\\textbf{Single reference authority.} One expected authority per
query, not every relevant source: inconsistency is a
reference mismatch, not a legal-relevance judgment.""",
"""\\textbf{Single reference authority.} One expected authority per
query: inconsistency is a
reference mismatch, not a relevance judgment."""),
("""\\textbf{Residual recovery gap.} At $k{=}100$, 17 of the 37 expected authorities
remain unrecovered; the \\texttt{2013\\_35}/\\texttt{1980\\_105} contrast shows
temporal room alone does not surface the authority.""",
"""\\textbf{Residual recovery gap.} At $k{=}100$, 17 of 37 expected authorities
remain unrecovered."""),
("""\\textbf{Year-level granularity.} Query dates have
year-level precision only, so same-year candidates
are conservatively excluded.""",
"""\\textbf{Year-level granularity.} Year-precision query dates mean
same-year candidates
are conservatively excluded."""),
("""\\textbf{Inference numerics.} Recomputed E3/E4 mean logits show bounded GPU
fp16 variation across runs (bounded at the fourth decimal in the
independent recomputation) that changed no decision, evidence selection, or
metric; strict serialized file hashes of E3/E4 outputs therefore differ while
substantive outputs agree.""",
"""\\textbf{Inference numerics.} Recomputed E3/E4 mean logits show bounded GPU
fp16 variation (fourth decimal) changing no decision, evidence, or
metric; serialized file hashes differ while
substance agrees."""),
("""\\textbf{Retrieval-equivalence scope.} BM25 rebuild equivalence is established
at ranking level --- identical corpus, parameters, and top-100 agreement on
all 30 evaluated queries --- not as byte-identical SQLite files, and it does
not generalize beyond the evaluated query set.""",
"""\\textbf{Retrieval-equivalence scope.} BM25 equivalence is ranking-level
(same corpus/parameters, top-100 agreement on
all 30 queries) --- not byte-identical files, not
beyond the evaluated set."""),
("""\\textbf{Non-independent explanation review.} The seven-case review is
author self-review. The superseding 14-case LLM comparison is exploratory
presentation evaluation, not human-subject evidence;
two runs produced identical outputs and are reported separately.""",
"""\\textbf{Non-independent review.} Seven-case author self-review;
14-case LLM comparison is exploratory,
not human-subject evidence."""),
("""\\textbf{Prototype scale.} Results apply to the frozen implementation and samples.
No production deployment is claimed or evaluated.""",
"""\\textbf{Prototype scale.} Frozen implementation and samples only;
no production deployment claimed."""),
("""The system is a legal-research aid, not an adjudicator or provider
of legal advice. E3/E4 predictions are experimental; a
human reviewer judges relevance, currency, authority, and
applicability \\cite{poojasingh2026}. Controls are fail-closed and negative results
(discarded runs, collision correction, key replacements) are preserved.""",
"""A legal-research aid, not an adjudicator:
E3/E4 predictions are experimental; human reviewers judge
relevance and applicability \\cite{poojasingh2026}. Fail-closed controls; negative results
preserved."""),
("""We built and evaluated a provenance-preserving, temporally constrained evidence
workflow for historical Indian Supreme Court research.""",
"""We built a provenance-preserving, temporally constrained evidence
workflow for Indian Supreme Court research."""),
("""The principal finding is a dissociation. Every one of 185 displayed citations
passed verification, with zero unsupported claims,
while 17 of
the 37 expected authorities were
absent at $k{=}100$.""",
"""Principal finding: all 185 displayed citations
passed verification with zero unsupported claims,
while 17 of
37 expected authorities were
absent at $k{=}100$."""),
("""The cross-corpus audit yields a transferable lesson: only 11 of
5{,}391 syntactic identifier matches between ILDC and the eCourts collection
were content-aligned.""",
"""Cross-corpus lesson: 11 of
5{,}391 ILDC--eCourts identifier matches
were content-aligned."""),
("""The supporting results are reported with their limits. The sparse TF--IDF baseline outperformed corrected InLegalBERT
under the frozen settings (1{,}503 cases). Inference-time evidence augmentation
reached 0.666667 accuracy and 0.603175 macro-F1 on the frozen 30-case subset
(0.648649 and 0.607347 on the combined 37), descriptively and under acknowledged
distribution shift. Presentation evidence is exploratory, not human preference.""",
"""Supporting results, with limits: sparse TF--IDF beat corrected InLegalBERT
(1{,}503 cases). Evidence augmentation
reached 0.666667/0.603175 on 30 cases
(0.648649/0.607347 on 37), descriptive only, under
distribution shift. Presentation evidence is exploratory."""),
("""\\textbf{Future work.} An era-balanced key of 75--100 cases for paired testing;
blinded review with independent raters; hybrid
dense--sparse retrieval for residual lexical misses; and evidence-sensitive
uncertainty language.""",
"""\\textbf{Future work.} Era-balanced key (75--100); blinded independent review;
hybrid retrieval; evidence-sensitive uncertainty language."""),
("""All configurations, seeds, model revisions, corpus identities, and evaluation
artifacts are frozen and machine-readable, including checkpoint-6318
(\\texttt{924a5bb9\\ldots dbdc773}). The implementation passes 81
tests and the documented
checks (14/14 documentation; freeze audit of 39 entries:
28 byte-exact, one line-ending-normalized, 10 metadata-differing; all reported
metrics verified identical).
The demo stack is covered by 8/8 Spring Boot service tests and 6/6 FastAPI
wrapper tests.""",
"""Configurations, seeds, revisions, corpus identities, and artifacts
are frozen and machine-readable, including checkpoint-6318
(\\texttt{924a5bb9\\ldots dbdc773}): 81
tests pass; 14/14 documentation checks; freeze audit of 39 entries
(28 byte-exact, one normalized, 10 metadata-differing; metrics identical);
demo covered by 8/8 Spring and 6/6 FastAPI tests."""),
]
fails = []
for i, (old, new) in enumerate(EDITS):
    c = t.count(old)
    if c != 1:
        fails.append((i, c))
        continue
    t = t.replace(old, new)
print("6p4: %d/%d, fails: %s" % (len(EDITS) - len(fails), len(EDITS), fails))
(R / "paper_master_6page.tex").write_text(t, encoding="utf-8")
