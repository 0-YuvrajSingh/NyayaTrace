"""Rebuild batch D3: compression edits (non-aborting)."""
from pathlib import Path

R = Path("/repo")
t = (R / "paper_master_final.tex").read_text(encoding="utf-8")

EDITS = [
("""E1 uses lowercased TF--IDF unigrams and bigrams with
sublinear term frequency, minimum document frequency two, $L_2$ normalisation,
and at most 100{,}000 features. Logistic-regression values
$C \\in \\{0.1, 1.0, 10.0\\}$ are compared by validation accuracy, with smaller $C$
breaking ties. The selected $C = 10.0$ pipeline is refitted once on eligible
training and validation cases and evaluated once on test data. Seed 202605.""",
"""E1 uses lowercased TF--IDF unigrams/bigrams (sublinear TF, min DF two, $L_2$,
100{,}000 features). Of
$C \\in \\{0.1, 1.0, 10.0\\}$, validation accuracy selected $C = 10.0$ (smaller $C$
ties); refit once on eligible
training plus validation and evaluated once on test. Seed 202605."""),
("""E2 fine-tunes \\texttt{law-ai/InLegalBERT} (revision
\\texttt{b5ecfed8}) with a new two-label head. It supersedes an
earlier 256-token prefix run that truncated 99.20\\% of eligible test inputs ---
a discarded result retained for traceability. Each facts-only document is
instead represented by overlapping 512-token windows with 50-token overlap.
Training uses three epochs, seed 202607, learning rate $2\\times10^{-5}$, weight
decay 0.01, warm-up ratio 0.1, and gradient
accumulation.""",
"""E2 fine-tunes \\texttt{law-ai/InLegalBERT} (revision
\\texttt{b5ecfed8}) with a new two-label head over overlapping 512-token windows with 50-token overlap.
Training uses three epochs, seed 202607, learning rate $2\\times10^{-5}$, weight
decay 0.01, warm-up ratio 0.1, and gradient
accumulation."""),
("""Candidate sources are checked against the alignment-gated crosswalk and a direct
self-match rule requiring at least 100 shared six-token occurrences and 80\\%
unique candidate-source phrase coverage. A non-learned selector then chooses up
to five passages in BM25 order, with at most one passage per source.""",
"""Candidate sources are checked against the alignment-gated crosswalk and a
self-match rule (100 shared six-token occurrences, 80\\%
source-phrase coverage). A non-learned selector then chooses up
to five passages in BM25 order, at most one per source."""),
("""Four populations are reported and never aggregated across kinds: 1{,}503 eligible fixed
ILDC test cases; a combined 37-case reference-evidence
population (Base-30 frozen key with 150 citations, Extension-7 additive cases
with 35, Combined-37 with 185), always stratified; and paired explanation-review
cases (seven formative author-reviewed pairs, superseded by the 14-case LLM
evaluation below).""",
"""Four populations are reported and never pooled: 1{,}503
ILDC test cases; Base-30 (150 citations), Extension-7
(35), Combined-37 (185), always stratified; and paired explanation-review
cases (seven formative pairs, superseded by the 14-case LLM
evaluation)."""),
("""The principal RQ3 evaluation is a blinded exploratory presentation comparison
by four LLM raters (Gemini, Claude Sonnet 4.6, DeepSeek, GPT-5.6 Luna) over 14
paired cases: the seven formative pairs plus all seven verified extension
cases, with no cherry-picking. Each rater scored five transparency
dimensions (1--5) with a forced preference, yielding 112
display ratings and 56 preferences. The structured presentation was preferred in 56/56 evaluations""",
"""The principal RQ3 evaluation is a blinded exploratory comparison
by four LLM raters (Gemini, Claude Sonnet 4.6, DeepSeek, GPT-5.6 Luna) over 14
paired cases on five transparency
dimensions (1--5) with a forced preference. The structured presentation was preferred in 56/56 evaluations"""),
("""This is explicitly \\emph{not} human evaluation: no independent rater
participated, no significance test was run, and nothing about human preference or legal correctness follows.
Two cautions apply. First, DeepSeek and GPT-5.6 Luna produced byte-identical
rating vectors, retained separately rather than
merged, so the unanimity partly reflects duplicated outputs.
Second, the seven-case self-review (means 4.57/2.71,
4.57/2.29, 4.43/2.86, 4.43/3.00; 7/7 structured) is formative,
non-independent evidence superseded above. Its durable output remains negative: generic
uncertainty wording did not adapt to
\\texttt{2013\\_35}, suggesting generic uncertainty language may not adapt
reliably to evidence quality.""",
"""This is explicitly \\emph{not} human evaluation: no independent rater
participated, no significance test was run, and nothing about human preference or legal correctness follows.
DeepSeek and GPT-5.6 Luna produced byte-identical
rating vectors, retained separately rather than
merged, so the unanimity partly reflects duplicated outputs. The seven-case self-review (7/7 structured) is formative,
non-independent evidence superseded above; its durable negative output is that generic
uncertainty wording did not adapt to
\\texttt{2013\\_35}."""),
("""The system is designed as a legal-research aid, not an adjudicator or a provider
of legal advice. E3/E4 predictions are experimental; the renderer states no
legal conclusion beyond supplied evidence, predictions stay separate, and a
human reviewer judges relevance, currency, authority, and
applicability \\cite{poojasingh2026}.""",
"""The system is a legal-research aid, not an adjudicator or provider
of legal advice. E3/E4 predictions are experimental; a
human reviewer judges relevance, currency, authority, and
applicability \\cite{poojasingh2026}. Controls are fail-closed, locators make
verification possible without trusting prose, and negative results
(discarded runs, superseded configurations, the collision
correction, key replacements, OCR exclusions, non-independent
review status) are preserved with populations and denominators kept separate."""),
("""Risk controls are fail-closed: missing dates, same-year ambiguity,
later dates, target identity, and duplication exclude evidence from display. A
citation must resolve to exact corpus text and the correct retrieval run;
altered or unsupported material is rejected. Stable locators
make verification possible without trusting the renderer's prose.

Governance also requires transparent negative results: discarded
runs, superseded configurations, the collision
correction, key replacements, OCR exclusions, and the non-independent
review status are preserved. Populations and denominators remain
separate, and alternative citations are not called irrelevant without
annotation.""",
""""""),
("""The principal finding is a dissociation. Every one of 185 displayed citations
across the combined 37 cases passed verification, with zero unsupported claims
across the 37 cases, while 17 of
the 37 expected authorities were
absent at $k{=}100$. Verification succeeded for what the system displayed; it did not
guarantee that the system found the expected authority. Legal-research systems
therefore benefit from explicit controls ---
but those controls must be evaluated \\emph{alongside}, never \\emph{instead of},
retrieval coverage and human review.""",
"""The principal finding is a dissociation. Every one of 185 displayed citations
passed verification, with zero unsupported claims,
while 17 of
the 37 expected authorities were
absent at $k{=}100$."""),
("""The supporting results are reported with their limits. On the 1{,}503-case
outcome task the sparse TF--IDF baseline outperformed corrected InLegalBERT
under the frozen settings --- a result about this experiment, not a general
verdict on legal-domain pre-training. Inference-time evidence augmentation
reached 0.666667 accuracy and 0.603175 macro-F1 on the frozen 30-case subset
(0.648649 and 0.607347 on the combined 37), descriptively and under acknowledged
distribution shift. The 14-case structured-presentation comparison is
exploratory LLM-rater evidence, not human preference; the seven-case
self-review beneath it is formative and non-independent.""",
"""The supporting results are reported with their limits. The sparse TF--IDF baseline outperformed corrected InLegalBERT
under the frozen settings (1{,}503 cases). Inference-time evidence augmentation
reached 0.666667 accuracy and 0.603175 macro-F1 on the frozen 30-case subset
(0.648649 and 0.607347 on the combined 37), descriptively and under acknowledged
distribution shift. Presentation evidence is exploratory, not human preference."""),
("""\\textbf{Future work.} An era-balanced key of 75--100 cases would support a
paired significance test (e.g., McNemar's); a blinded review with
independent raters and agreement reporting (e.g., Fleiss'
$\\kappa$) would replace the formative explanation evidence; hybrid
dense--sparse retrieval would test whether semantic retrieval closes
residual lexical misses under the present controls; and evidence-sensitive
uncertainty language would address the exposed
calibration weakness.""",
"""\\textbf{Future work.} An era-balanced key of 75--100 cases for paired testing;
blinded review with independent raters; hybrid
dense--sparse retrieval for residual lexical misses; and evidence-sensitive
uncertainty language."""),
("""A minimal connected local research demo (React 18 + TypeScript UI,
Spring Boot 3.2.5 orchestration API, FastAPI wrapper around the frozen
pipeline) exposes the E4 evidence path with bearer-token authentication,
per-request audit records, and experiment-metadata references; the FastAPI
layer delegates every research step to the frozen implementation and the
static frozen-artifact viewer is retained as a fallback. The stack binds to
loopback only and is not a production, multi-tenant, or autonomous system.""",
"""A minimal local research demo (React UI,
Spring Boot 3.2.5 API, FastAPI wrapper) exposes the E4 evidence path. The stack binds to
loopback only."""),
]
fails = []
for i, (old, new) in enumerate(EDITS):
    c = t.count(old)
    if c != 1:
        fails.append((i, c))
        continue
    t = t.replace(old, new)
print(f"D3: {len(EDITS) - len(fails)}/{len(EDITS)}, fails: {fails}")
(R / "paper_master_final.tex").write_text(t, encoding="utf-8")
