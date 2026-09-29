"""Rebuild batch D4: captions, figures, defs, remaining trims (non-aborting)."""
from pathlib import Path

R = Path("/repo")
t = (R / "paper_master_final.tex").read_text(encoding="utf-8")

EDITS = [
("""\\caption{Operational definitions used throughout the frozen evaluation.}""",
 """\\caption{Operational definitions (frozen evaluation).}"""),
("""\\caption{RQ1 retrieval and evidence-augmented prediction by stratum. The
combined row is the principal evaluation; strata are never pooled silently.}""",
 """\\caption{RQ1 retrieval and prediction by stratum (combined row principal).}"""),
("""\\caption{Evidence recovery and integrity on the frozen Base-30 answer-key
stratum ($n=30$
queries; 150 displayed citations). Combined-37 values are reported in
Table~\\ref{tab:rq1strata} and the surrounding text.}""",
 """\\caption{Evidence recovery and integrity, Base-30 (30
queries; 150 citations).}"""),
("""\\caption{Accuracy and macro-F1 for E1, corrected E2 under both pooling rules,
and the majority baseline on the eligible ILDC test population ($n=1{,}503$).}""",
 """\\caption{Accuracy and macro-F1 on the eligible ILDC test population ($n=1{,}503$).}"""),
("""\\caption{Expected-authority recovery on the combined reference set
($n=37$): 12 selected, eight retrieved but unselected (three
base, five extension), 17 absent at $k{=}100$.}""",
 """\\caption{Expected-authority recovery ($n=37$): 12 selected, eight retrieved but unselected,
17 absent at $k{=}100$.}"""),
("""\\caption{Displayed-evidence integrity, combined $n=37$ (185 citations): all
grounding and
provenance checks passed,
with no temporal violations or unsupported claims. Base-30
contributes 150/150.}""",
 """\\caption{Displayed-evidence integrity ($n=37$, 185 citations): all checks passed.}"""),
("""\\caption{Outcome prediction. Populations are distinct and not a
like-for-like leaderboard.}""",
 """\\caption{Outcome prediction (distinct populations; not a leaderboard).}"""),
("""\\includegraphics[width=0.80\\columnwidth]{figures/fig2_funnel.pdf}""",
 """\\includegraphics[width=0.62\\columnwidth]{figures/fig2_funnel.pdf}"""),
("""\\includegraphics[width=0.80\\columnwidth]{figures/fig3_integrity.pdf}""",
 """\\includegraphics[width=0.62\\columnwidth]{figures/fig3_integrity.pdf}"""),
("""The evidence corpus is an eCourts-derived collection of Indian Supreme Court
judgments covering 1950--2020, supplying the metadata absent
from ILDC: citations, exact decision dates, court and case identifiers, source
paths, and page and character locators. Of 39{,}069 English""",
"""The evidence corpus is an eCourts-derived collection of Indian Supreme Court
judgments covering 1950--2020. Of 39{,}069 English"""),
("""A full audit found the stored text valid UTF-8, but 15 PDF instances
(representing 14 source IDs) had missing or badly corrupted embedded text,
concentrated in image-backed 1980s/1990s Reports plus one mojibake-affected
2018 file. Fixed checks covered absent
embedded text, control characters, mojibake markers, visible-ASCII ratio, and
English-token ratio.""",
"""A full audit found the stored text valid UTF-8, but 15 PDF instances
(representing 14 source IDs) had missing or badly corrupted embedded text."""),
("""\\textbf{Scope.} English-language Indian Supreme Court judgments
only; no other Indian languages, High Court or lower-court
material, separately versioned statutes, or cross-jurisdictional transfer.""",
"""\\textbf{Scope.} English-language Indian Supreme Court judgments
only; no other languages, lower courts,
statutes, or cross-jurisdictional transfer."""),
("""\\textbf{Answer-key size and era concentration.} Evidence evaluation rests on
30 frozen cases, extended additively to 37 with seven later
verified cases; 13 of the base 30 are from
the 1980s. The combined set is neither large nor era-balanced and should not
be read as representative of the ILDC test set or of
Indian legal research generally --- the primary constraint on
generality. The shared 14-case facts-sufficiency filter likewise narrows the
prediction population to inputs with adequate pre-decision material.""",
"""\\textbf{Answer-key size and era concentration.} Evidence evaluation rests on
30 frozen cases, extended additively to 37;
13 of the base 30 are from
the 1980s. The combined set is neither large nor era-balanced and should not
be read as representative of the ILDC test set or of
Indian legal research generally."""),
("""\\textbf{Single reference authority.} One expected authority per
query, not every relevant source: inconsistency is a reproducible
reference mismatch, not a substantive legal-relevance judgment.""",
"""\\textbf{Single reference authority.} One expected authority per
query, not every relevant source: inconsistency is a
reference mismatch, not a legal-relevance judgment."""),
("""\\textbf{Residual recovery gap.} At $k{=}100$, 17 of the 37 expected authorities
still went unrecovered; the \\texttt{2013\\_35}/\\texttt{1980\\_105} contrast shows
temporal room alone does not surface the authority. This limited comparison
does not establish a causal attribution for the remaining gap.""",
"""\\textbf{Residual recovery gap.} At $k{=}100$, 17 of the 37 expected authorities
remain unrecovered; the \\texttt{2013\\_35}/\\texttt{1980\\_105} contrast shows
temporal room alone does not surface the authority."""),
("""\\textbf{Year-level temporal granularity.} ILDC query dates have
year-level precision only, so any candidate sharing a query's year
is excluded rather than risk admitting a source that actually postdates it --
a conservative choice that can discard genuinely eligible evidence. Day-level
dates would require manually checking each case against a primary
source; the limitation
therefore sits in the dataset, not in how the pipeline parses dates.""",
"""\\textbf{Year-level temporal granularity.} Query dates have
year-level precision only, so any same-year candidate
is conservatively excluded."""),
("""\\textbf{Non-independent explanation review.} The seven-case review is a
non-random author self-review. The superseding 14-case LLM comparison is exploratory
presentation evaluation by four model raters, not human-subject evidence;
two runs produced identical outputs and are reported separately
rather than merged, so even unanimity partly reflects
duplicated runs.""",
"""\\textbf{Non-independent explanation review.} The seven-case review is
author self-review. The superseding 14-case LLM comparison is exploratory
presentation evaluation, not human-subject evidence;
two runs produced identical outputs and are reported separately."""),
("""\\textbf{Prototype scale.} Results apply to the frozen implementation and samples
rather than to all users, courts, domains, or changing corpora. No production
deployment is claimed or evaluated.""",
"""\\textbf{Prototype scale.} Results apply to the frozen implementation and samples.
No production deployment is claimed or evaluated."""),
("""All configurations, seeds, model revisions, corpus identities, and evaluation
artifacts are frozen and machine-readable, including checkpoint-6318
(\\texttt{924a5bb9\\ldots dbdc773}) with a stable replay hash. The implementation passes 81 automated
research-pipeline tests (75 host-runnable plus 6
transformer/torch-only unit tests) and the documented
reproducibility checks (14/14 documentation checks and a freeze audit of 39 recorded
entries: 28 byte-exact, one line-ending-normalized, and 10 differing only in
non-scientific metadata, with all reported metrics verified identical;
per-file evidence in the repository audit). Separately, the
local demo stack is covered by 8/8 Spring Boot service tests, 6/6 FastAPI
wrapper tests; these exercise orchestration and contracts only, never the frozen
scientific results.""",
"""All configurations, seeds, model revisions, corpus identities, and evaluation
artifacts are frozen and machine-readable, including checkpoint-6318
(\\texttt{924a5bb9\\ldots dbdc773}). The implementation passes 81
tests and the documented
checks (14/14 documentation; freeze audit of 39 entries:
28 byte-exact, one line-ending-normalized, 10 metadata-differing; all reported
metrics verified identical).
The demo stack is covered by 8/8 Spring Boot service tests and 6/6 FastAPI
wrapper tests."""),
]
fails = []
for i, (old, new) in enumerate(EDITS):
    c = t.count(old)
    if c != 1:
        fails.append((i, c))
        continue
    t = t.replace(old, new)
print(f"D4: {len(EDITS) - len(fails)}/{len(EDITS)}, fails: {fails}")
(R / "paper_master_final.tex").write_text(t, encoding="utf-8")
