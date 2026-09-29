"""Rebuild paper_master_final.tex from paper_master_revised.tex by replaying all approved edits."""
import shutil
from pathlib import Path

R = Path("/repo")
shutil.copy(R / "paper_master_revised.tex", R / "paper_master_final.tex")
t = (R / "paper_master_final.tex").read_text(encoding="utf-8")

EDITS = [
# --- citation fixes ---
("""the matter, or may never have been retrieved. The order copy cited here
reports a 2026 Supreme Court of India ruling overturning tribunal findings
built on exactly these defects, making citation verifiability a functional
requirement. We present an""",
"""the matter, or may never have been retrieved. A 2026 Supreme Court of India
ruling (2026 INSC 668) overturned tribunal findings built on exactly these
defects. We present an"""),
("""The problem is no longer confined to the literature. According to the order
copy cited here, in \\emph{Pooja Ramesh Singh""",
"""The problem is no longer confined to the literature. In \\emph{Pooja Ramesh Singh"""),
("""\\& Anr.}, 2026 INSC 668, the Supreme Court of""",
"""\\& Anr.}, 2026 INSC 668 (Civil Appeal
No.\\ 11950 of 2025, decided 2 July 2026), the Supreme Court of"""),
("""\\& Anr.}, 2026 INSC 668, 2026. Order copy:
\\url{https://ibbi.gov.in/uploads/order/8e1ccab8f7f445f81034223c1d0fe7b9.pdf}.""",
"""\\& Anr.}, 2026 INSC 668 (Civil Appeal No.\\ 11950 of 2025, decided 2 July 2026),
2026. Court PDF:
\\url{https://www.sci.gov.in/sci-get-pdf/?diary_no=523382025&from=latest_judgements_order&order_date=2026-07-02&type=j}."""),
("""V. R. Karna, R. R. M., B. S. Babu, N. S., M. M., and H. V.,
``A Hybrid RAG-LLaMA Framework for Scalable and Accurate Interpretation of Legal
Texts,'' \\emph{Applied Artificial Intelligence}, vol.\\ 40, no.\\ 1, art.\\
2626097, 2026.""",
"""V. R. Karna, R. R. M., B. S. Babu, \\emph{et al.},
``A Hybrid RAG-LLaMA Framework for Scalable and Accurate Interpretation of Legal
Texts,'' \\emph{Applied Artificial Intelligence}, vol.\\ 40, no.\\ 1, art.\\
2626097, 2026. DOI: \\url{https://doi.org/10.1080/08839514.2026.2626097}."""),
# --- compression round 1 ---
("""The boundary against
the closest work is as follows. We claim neither the first legal RAG system, nor the first""",
"""We claim neither the first legal RAG system, nor the first"""),
("""Jurisdictions, tasks, corpora, and denominators differ, so no external system is
used as a numerical baseline. Per-work boundaries: ILDC/CJPE
\\cite{malik2021} supplies the prediction setting and splits (we add a
separate provenance-bearing corpus without reproducing its architecture);
InLegalBERT \\cite{paul2023} motivates the neural baseline (we correct
truncation via chunk-and-pool without assuming it must win); TaxFlow
\\cite{taxflow2026} shares legal-retrieval concerns (statutory validity; we address
precedent identity, passage provenance, and a verified key instead);
CaseFacts \\cite{casefacts2026} shows validity evolves with noisy open
retrieval (we verify identity, eligibility, and provenance from case facts);
LexTime \\cite{lextime2025} treats event ordering, whereas we enforce
availability through metadata before ranking.""",
"""Jurisdictions, tasks, corpora, and denominators differ, so no external system is
used as a numerical baseline. ILDC \\cite{malik2021} supplies the prediction
setting and splits; InLegalBERT \\cite{paul2023} motivates the neural baseline;
TaxFlow \\cite{taxflow2026} addresses statutory validity rather than precedent
identity and passage provenance; CaseFacts \\cite{casefacts2026} and LexTime
\\cite{lextime2025} target open-retrieval validity and event ordering, whereas we
enforce availability through metadata before ranking."""),
("""The system comprises four auditable layers. E1 is the traditional TF--IDF plus
logistic-regression outcome baseline; E2 is the facts-only InLegalBERT outcome
baseline. E3 is the retrieval/evidence-grounded branch, and E4 is the
verification, provenance, and structured-explanation bundle applied to that
branch. E2 is not a retrieval baseline. Retrieval quality is evaluated against
the predefined authority/evidence key; outcome prediction is secondary.

\\textbf{1. Corpus and alignment layer.} ILDC splits supply prediction cases
and labels. Cleaned eCourts chunks retain stable source, date, citation, court,
PDF, page, and character provenance. A content-aligned crosswalk plus a runtime
content check control target-case leakage.

\\textbf{2. Outcome branch.} A shared facts-only extractor feeds sparse linear
baseline (E1) and InLegalBERT chunk-and-pool model (E2). These baselines
produce binary predictions and never retrieve external evidence.

\\textbf{3. Evidence branch (E3).} Facts-only text is converted to salient
terms, matched through BM25 under pre-ranking temporal eligibility, and narrowed
to five source-diverse passages rendered in a fixed
evidence-linked structure.

\\textbf{4. Verification and reporting layer (E4).} Each displayed record
is verified against the corpus and the recorded retrieval run; duplicate
and temporal rules are enforced; verified sources are compared
with the source-first answer key. Versioned artifacts preserve
metrics, failures, and configuration provenance.

The evidence renderer is extractive: material legal text is displayed verbatim, and its
evidence-bound conclusion uses fixed, non-inferential wording tied to evidence
identifiers. The renderer cannot retrieve, rerank, invent an authority,
paraphrase a material proposition, or infer an outcome. Outcome prediction is produced separately by
the prediction branch.""",
"""Four auditable layers implement the design. A corpus and alignment layer links
ILDC cases to dated eCourts passages with content-checked deduplication. An
outcome branch (E1 sparse linear, E2 InLegalBERT chunk-and-pool) predicts from
facts only and never retrieves. An evidence branch (E3) retrieves BM25 passages
under pre-ranking temporal eligibility and renders five source-diverse verbatim
passages. A verification layer (E4) checks each displayed record against the
corpus and the recorded retrieval run. The renderer is extractive and cannot
retrieve, paraphrase material text, or infer outcomes; prediction stays separate."""),
("""This paper treats that requirement as the primary design constraint over
historical Indian Supreme Court judgments: case facts are retrieved with
stable locators,
duplicates excluded, only
selected verbatim passages rendered, each citation verified against
the persisted corpus and retrieval run, and outcome prediction kept in a
separate field that never alters the evidence-bound conclusion.""",
"""This paper treats that requirement as the primary design constraint over
historical Indian Supreme Court judgments: retrieved facts carry stable
locators, duplicates are excluded, only verbatim passages are rendered,
and each citation is verified against the persisted corpus and retrieval run."""),
("""For RQ3, the implemented comparison holds the underlying evidence and citations
constant and compares structured with unstructured presentation. It evaluates
presentation transparency only; it does not independently establish a measurable
prediction or retrieval-performance degradation or non-degradation effect.""",
"""For RQ3, the implemented comparison holds the underlying evidence and citations
constant and compares structured with unstructured presentation
(transparency only)."""),
("""This split follows the information actually available in each source. ILDC
supports fixed-split outcome prediction but exposes only a year in the case
identifier and lacks the citation and passage provenance that verification
requires. The eCourts collection supports dated, traceable retrieval but is not
used as a substitute outcome-label benchmark. Cross-corpus links are drawn only
after the alignment checks described below.""",
"""This split follows the information actually available in each source. ILDC
supports fixed-split outcome prediction but lacks citation and passage
provenance; the eCourts collection supports dated, traceable retrieval but is
not an outcome-label benchmark. Cross-corpus links are drawn only
after the alignment checks described below."""),
("""Only flagged instances were re-rendered and processed with English Tesseract OCR
at 250\\,DPI \\cite{smith2007}. Twelve passed the same post-OCR quality gate and
were restored; three single-page PDFs remained below threshold and were
transparently excluded rather than forced into the index. Raw PDFs were
preserved unchanged, exclusions were recorded, and the provenance store and BM25
index were rebuilt from the accepted corpus.""",
"""Only flagged instances were re-rendered and processed with English Tesseract OCR
at 250\\,DPI \\cite{smith2007}. Twelve passed the post-OCR quality gate and
were restored; three single-page PDFs remained below threshold and were
excluded. Raw PDFs were preserved and the index rebuilt from the accepted corpus."""),
("""The corrected pipeline treats identifier equality as candidate generation only.
A reusable gate evaluates title or party identity together with direct six-token
phrase overlap before any mapping may drive deduplication or retrieval
exclusion. Combining syntactic and title/party candidates yielded 8{,}927
deduplicated pairs, of which 1{,}304 were accepted and 7{,}623 rejected.
Retrieval additionally applies a full-document self-match safeguard, so that an
unmapped copy of the query judgment can be removed without suppressing an
earlier authority merely quoted at length by the later judgment.""",
"""The corrected pipeline treats identifier equality as candidate generation only.
A reusable gate evaluates title/party identity with direct six-token
phrase overlap before any mapping drives deduplication or
exclusion. Combining syntactic and title/party candidates yielded 8{,}927
deduplicated pairs (1{,}304 accepted, 7{,}623 rejected).
Retrieval additionally applies a full-document self-match safeguard, so an
unmapped copy of the query judgment is removed without suppressing an
earlier authority quoted at length by the later judgment."""),
("""The identifier-collision discovery triggered a read-only audit of the
then-current mappings: 20 passed, nine resolved sources failed direct content
alignment, and one source was unresolved. One case was relinked to a
content-aligned source and the other nine flagged records were replaced by new
fixed-test cases, yielding a final audit of 30/30 direct-content passes.""",
"""The identifier-collision discovery triggered a read-only audit of the
then-current mappings: 20 passed, nine failed direct content
alignment, and one was unresolved. One case was relinked
and the other nine replaced by new
fixed-test cases, yielding 30/30 direct-content passes."""),
("""same gates, without modifying the original 30-case key
(listed in Section~\\ref{sec:results}). Three further
candidates were held back as needing review and are not part of
any evaluation. The combined 37-case population is therefore a later expanded
analysis, not the original frozen base; all results below retain
Base-30, Extension-7, and Combined-37 strata.""",
"""same gates, without modifying the original 30-case key.
Three further candidates were held back as needing review. The combined 37-case
population is a later expanded analysis, not the frozen base; results below
retain Base-30, Extension-7, and Combined-37 strata."""),
("""E1 and E2 share the extraction configuration \\texttt{ildc-\\allowbreak predecision-\\allowbreak facts-\\allowbreak v1}.
The extractor retains text preceding the earlier of a recognised dispositive cue
and 60\\% of the document, moving the boundary to a preceding sentence end when
sufficient text remains. Cases below 10\\% retention or 100 words are excluded.
Neither prediction path uses retrieval. Model and threshold selection uses
validation data only; the held-out test split is evaluated once, after
selection.""",
"""E1 and E2 share the extraction configuration \\texttt{ildc-\\allowbreak predecision-\\allowbreak facts-\\allowbreak v1}: text preceding the earlier of a recognised dispositive cue
and 60\\% of the document, sentence-aligned where possible. Cases below 10\\% retention or 100 words are excluded.
Neither prediction path uses retrieval. Selection uses
validation data only; the held-out test split is evaluated once."""),
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
("""The query builder \\texttt{tfidf-\\allowbreak segment-\\allowbreak salient-\\allowbreak terms-\\allowbreak v1} segments the full
facts-only input, removes procedural-report boilerplate, scores terms
deterministically, retains section and article cues, and emits at most 32 unique
terms. These query a SQLite FTS5 BM25 index backed by PostgreSQL provenance.

The frozen configuration is
\\texttt{week11-\\allowbreak bm25-\\allowbreak salient-\\allowbreak terms-\\allowbreak preranked-\\allowbreak temporal-\\allowbreak v3}: only judgments with decision year strictly earlier than the
query year enter the candidate relation \\emph{before} BM25 ordering and the
top-100 cutoff, so the full depth is spent on eligible material rather than
discarded ineligible depth.""",
"""The query builder (\\texttt{tfidf-segment-salient-terms-v1}) segments the facts-only input, removes procedural-report boilerplate, scores terms
deterministically, retains section/article cues, and emits at most 32 unique
terms for a SQLite FTS5 BM25 index backed by PostgreSQL provenance.

The frozen configuration (\\texttt{week11-bm25-salient-terms-preranked-temporal-v3}) admits only judgments with decision year strictly earlier than the
query year into the candidate relation \\emph{before} BM25 ordering and the
top-100 cutoff, so the full depth is spent on eligible material."""),
]

for i, (old, new) in enumerate(EDITS):
    if t.count(old) != 1:
        print(f"EDIT {i}: found {t.count(old)} occurrences (expected 1). ABORT.")
        raise SystemExit(1)
    t = t.replace(old, new)
print(f"batch1 ok: {len(EDITS)} edits")
(R / "paper_master_final.tex").write_text(t, encoding="utf-8")
