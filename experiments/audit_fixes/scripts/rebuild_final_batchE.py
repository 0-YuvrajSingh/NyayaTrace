"""Rebuild batch E: defs cells + remaining prose cuts (non-aborting).

LaTeX table row endings (\\) are placed at line end so no backslash
precedes a closing quote.
"""
from pathlib import Path

R = Path("/repo")
t = (R / "paper_master_final.tex").read_text(encoding="utf-8")

BS = chr(92)
NL = chr(10)
ROW = BS + BS  # LaTeX \\ row ending

def row(cell):
    return cell + " " + ROW

OLD_DEFS = NL.join([
    "Facts-only input &",
    "Text retained before the earlier of a recognised dispositive cue and a 60\\%",
    "character cap, sentence-aligned where possible; inputs below 10\\% retention or",
    "100 words are excluded " + ROW,
])
NEW_DEFS = NL.join([
    "Facts-only input &",
    "Text before the earlier of a recognised dispositive cue and a 60\\%",
    "character cap; inputs below 10\\% retention or",
    "100 words are excluded " + ROW,
])

pairs = [(OLD_DEFS, NEW_DEFS)]

OLD2 = NL.join([
    "Temporal existence &",
    "The source has a parseable exact decision date in corpus metadata " + ROW,
])
NEW2 = NL.join([
    "Temporal existence &",
    "The source has a parseable exact decision date " + ROW,
])
pairs.append((OLD2, NEW2))

OLD3 = NL.join([
    "Temporal effectiveness &",
    "The eligibility predicate is applied inside the BM25 candidate relation before",
    "ranking and \\texttt{LIMIT 100}, so ineligible sources cannot consume returned",
    "depth " + ROW,
])
NEW3 = NL.join([
    "Temporal effectiveness &",
    "Eligibility is applied inside the BM25 candidate relation before",
    "ranking and \\texttt{LIMIT 100} " + ROW,
])
pairs.append((OLD3, NEW3))

OLD4 = NL.join([
    "Recall@100 &",
    "Share of answer-key cases whose predefined authority occurs anywhere in the",
    "returned top-100 candidates " + ROW,
])
NEW4 = NL.join([
    "Recall@100 &",
    "Share of cases whose predefined authority occurs in the",
    "returned top-100 " + ROW,
])
pairs.append((OLD4, NEW4))

OLD5 = NL.join([
    "Recall@5 &",
    "Share of answer-key cases whose predefined authority is among the five selected",
    "and displayed sources " + ROW,
])
NEW5 = NL.join([
    "Recall@5 &",
    "Share of cases whose predefined authority is among the five selected",
    "sources " + ROW,
])
pairs.append((OLD5, NEW5))

OLD6 = NL.join([
    "Provenance validity &",
    "A displayed item reproduces the stored source ID, citation, decision date,",
    "court, PDF/page/character locator, exact passage, and retrieval-run membership " + ROW,
])
NEW6 = NL.join([
    "Provenance validity &",
    "A displayed item reproduces the stored source ID, citation, decision date,",
    "court, locator, exact passage, and retrieval-run membership " + ROW,
])
pairs.append((OLD6, NEW6))

OLD7 = NL.join([
    "Citation groundedness &",
    "Every material displayed proposition is verbatim text of a supplied evidence",
    "passage and links to that evidence item " + ROW,
])
NEW7 = NL.join([
    "Citation groundedness &",
    "Every displayed material proposition is verbatim text of a supplied passage",
    "linked to that evidence item " + ROW,
])
pairs.append((OLD7, NEW7))

OLD8 = NL.join([
    "Authority consistency &",
    "A verified displayed source matches the answer-key authority by stable source",
    "ID, normalised citation, or normalised title plus exact decision date " + ROW,
])
NEW8 = NL.join([
    "Authority consistency &",
    "A displayed source matches the answer-key authority by stable source",
    "ID, normalised citation, or title plus exact decision date " + ROW,
])
pairs.append((OLD8, NEW8))

pairs.append((
    "Candidate sources are checked against the alignment-gated crosswalk and a direct\n"
    "self-match rule requiring at least 100 shared six-token occurrences and 80\\%\n"
    "unique candidate-source phrase coverage. A non-learned selector then chooses up\n"
    "to five passages in BM25 order, with at most one passage per source.",
    "Candidate sources are checked against the alignment-gated crosswalk and a\n"
    "self-match rule (100 shared six-token occurrences, 80\\%\n"
    "source-phrase coverage). A non-learned selector then chooses up\n"
    "to five passages in BM25 order, at most one per source.",
))
pairs.append((
    "Four populations are reported and never aggregated across kinds: 1{,}503 eligible fixed\n",
    "Four populations are reported and never pooled: 1{,}503\n",
))
pairs.append((
    "On the 1{,}503-case population (Table~\\ref{tab:outcome}), sparse E1 reached accuracy 0.61344 and macro-F1 0.612342,\n"
    "exceeding corrected E2 mean-logit pooling at 0.596806 and 0.592358. E2's secondary\n"
    "majority-vote aggregation reached 0.6015 and 0.5937. All primary models exceeded\n",
    "On the 1{,}503-case population (Table~\\ref{tab:outcome}), sparse E1 reached accuracy 0.61344 and macro-F1 0.612342,\n"
    "exceeding corrected E2 mean-logit pooling at 0.596806 and 0.592358 (majority vote\n"
    "0.6015 and 0.5937). All primary models exceeded\n",
))
pairs.append((
    "The supporting results are reported with their limits. On the 1{,}503-case\n"
    "outcome task the sparse TF--IDF baseline outperformed corrected InLegalBERT\n"
    "under the frozen settings --- a result about this experiment, not a general\n"
    "verdict on legal-domain pre-training. Inference-time evidence augmentation\n",
    "The supporting results are reported with their limits. The sparse TF--IDF baseline outperformed corrected InLegalBERT\n"
    "under the frozen settings (1{,}503 cases). Inference-time evidence augmentation\n",
))
pairs.append((
    "distribution shift. The 14-case structured-presentation comparison is\n"
    "exploratory LLM-rater evidence, not human preference; the seven-case\n"
    "self-review beneath it is formative and non-independent.",
    "distribution shift. Presentation evidence is exploratory, not human preference.",
))

fails = []
for i, (old, new) in enumerate(pairs):
    c = t.count(old)
    if c != 1:
        fails.append((i, c))
        continue
    t = t.replace(old, new)
print("E: %d/%d, fails: %s" % (len(pairs) - len(fails), len(pairs), fails))
(R / "paper_master_final.tex").write_text(t, encoding="utf-8")
