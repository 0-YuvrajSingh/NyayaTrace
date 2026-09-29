# Humanization and Scientific Freeze Edit Log

**Date:** 2026-09-29 (Prompt 24 initial edits; Prompt 25 final corrections)
**Input Manuscript Hash (pre-Prompt 24):** `FADC2392166664C60FB18365557BF065123AD62DE476F81A94DA3FAC236F961C`
**Post-Prompt-24 Hash:** `E8626177248462AD461CF2E04728889F2281E1A0F263658689015C7C29817308`
**Final Manuscript Hash (post-Prompt 25):** `B3F8AA630FE859B4536629377338C90052C9BB938BB982D6AB71BDC55FCD1E0D`
**Final PDF SHA-256:** `21351DA44C2E3A759C1195EC9613ECB2297FA3CEE291FFFF19C21D9B60D6DA09`
**Page count:** 6 (CONFIRMED — xdvipdfmx `[1][2][3][4][5][6]`)

## Sections Reviewed
- Abstract
- Introduction
- Problem Formulation
- Corpus Construction
- System Design
- Method
- Citation and Provenance Protocol
- Results
- Responsible Use and Governance
- Conclusion and Future Work
- Reproducibility

## Categories of Edits
1. **Scientific Claim Freeze:** Removed claims and numbers tied to non-independently verified extensions (Extension-7, Combined-37), exploratory LLM reviews, and OCR precise counts.
2. **Structural Humanization:** Improved flow and rhythm in the Abstract, Introduction, and Conclusion to remove generic boilerplate and repetitive templates.
3. **Technical Precision/Ownership:** Adjusted sentence framing to clarify the nature of specific findings and avoid ambiguous descriptions.

## Representative Examples

### Example 1: Removing Generic Boilerplate (Humanization)
- **Before:** `The central finding is a dissociation: all 150 displayed base citations cleared verification with no unsupported claim, yet 15 of 30 expected authorities never appeared in the top 100.`
- **After:** `Our primary finding highlights a clear dissociation: while all 150 displayed citations passed verification without a single unsupported claim, 15 of the 30 expected authorities failed to appear within the top 100 retrieved results.`
- **Meaning Changed:** No.
- **Goal:** Improve sentence rhythm and scholarly tone while preserving all numeric claims.

### Example 2: Emphasizing Technical Ownership
- **Before:** `We report three independently replayed findings. First, naive ILDC--eCourts identifier matching is unsafe: 11 of 5{,}391 syntactic matches survived alignment.`
- **After:** `We report three independently replayed findings. First, naive ILDC--eCourts identifier matching proves unsafe, as only 11 out of 5{,}391 syntactic matches survived strict content alignment.`
- **Meaning Changed:** No.
- **Goal:** Added precise phrasing ("proves unsafe, as only", "strict content alignment") to sound like researchers explaining their process natively.

### Example 3: Unverified Result Removal (Scientific Freeze)
- **Before:** `The Extension-7 stratum (0/7 top-5; five top-100 recoveries; 35/35 verified) and the Combined-37 row are reported from frozen artifacts and were not independently replayed.` (plus matching table rows).
- **After:** *[Entirely removed from manuscript and tables]*
- **Meaning Changed:** Yes. The scope of results is narrowed to the verified Base-30.
- **Goal:** Comply with the requirement to remove quantitative claims not supported by independent replay.

### Example 4: Abstracting Unverified Metrics
- **Before:** `Twelve passed the post-OCR quality gate and were restored; three single-page PDFs remained below threshold and were excluded.`
- **After:** `Instances passing a post-OCR quality gate were restored.`
- **Meaning Changed:** Yes (removed exact counts).
- **Goal:** Removed unverified OCR counts (not independently replayed) while preserving the necessary procedural description of corpus recovery.

## Citation Changes
- No citations were added or removed. 
- The reference to `smith2007` (Tesseract OCR) was explicitly retained as it accurately reflects the pipeline component, even though the unverified success/failure counts were removed.

## Factual Corrections
- Removed all mentions of "RQ3" regarding the structured explanation format since the LLM-evaluator analysis was an exploratory, non-independent review, and evaluating presentation was deemed outside the strictly verified quantitative scope.

## Explicitly Preserved Technical Statements
- **BM25 equivalence scope:** The clarification that the BM25 rebuild was identical at the ranking level (top 100 for evaluated queries) rather than byte-for-byte SQLite equality was retained exactly as it accurately reflects the limit of the reproduction claim.
- **Leakage:** The language confirming zero temporal violations and zero self-matches was retained exactly without expanding it into a generalized "guaranteed leakage-free" claim.
- **Outcome Metrics:** All numbers related to the 1,503-case split baseline accuracy (0.61344 and 0.596806) were preserved verbatim as they are established by E1 and E2 reproducible evidence.

---
## Prompt 29 (Final Direct Repository Application)

**Date:** 2026-09-29
**Final TEX SHA-256:** 0CE6A6B0FF0205ED50921BEB19BF106370B43D1A27A11903145BD2AAB817238A
**Final PDF SHA-256:** F4C6225778C888C3B0984A750C0D7E65BEB19829FF61B46DFA0B553EAA6B131B
**Page Count:** 6 (Confirmed via tectonic exit 0, exactly [1][2][3][4][5][6])
**Overfull Hboxes:** 0

### Direct Edits Applied

1. **Abstract Scientific Correction:**
   * **Before:** "We report three independently replayed findings. First, naive ILDC--eCourts identifier matching proves unsafe, as only 11 out of 5{,}391..."
   * **After:** "We report three main findings, supported by independent replay and source-side audit. First, naive ILDC--eCourts identifier matching proves unsafe: only 11 of 5{,}391..."
   * **Meaning:** Corrected scientific provenance (the 5391->11 is a source-side corpus audit, not independent replay); applied stylistic humanization ("unsafe: only" instead of "unsafe, as only").

2. **Contributions (Population Clarification):**
   * **Before:** "...and presentation are reported on their own populations"
   * **After:** "...and outcome prediction are reported on their own populations"
   * **Meaning:** Removed obsolete presentation evaluation claim to match the scientific freeze.

3. **Scope (Population Count Correction):**
   * **Before:** "...four non-pooled populations (1{,}503 outcome cases; 30 frozen evidence cases..."
   * **After:** "...Two populations are evaluated and never pooled: 1{,}503 outcome cases and the 30 frozen evidence cases (Base-30)."
   * **Meaning:** Fixed incorrect statement of 4 populations to correctly state 2 populations, completely segregating outcome vs. evidence.

4. **Problem Formulation (Presentation Clarification):**
   * **Before:** "...and presentation (does structure aid inspection?)."
   * **After:** "...Presentation asks whether the structure aids inspection; we do not evaluate it here."
   * **Meaning:** Kept presentation as a conceptual evidence task dimension but explicitly disclaimed it from this evaluation. Converted a long fragmented list into declarative sentences.

5. **Method E4 (Structural Humanization):**
   * **Before:** "Each displayed item must exist in the corpus, reproduce exact passage and provenance, belong to the recorded run, avoid the query and duplicates, and pre-date the query year; any failure rejects the citation."
   * **After:** "Each displayed item must exist in the corpus and reproduce its stored passage and provenance. It must also belong to the recorded run, exclude the query and duplicates, and pre-date the query year; any failure rejects the citation."
   * **Meaning:** Split a long 5-part run-on requirement sentence into two cleaner, active constraints without altering the exact rigorous requirements.

6. **Results Caveat (Structural Humanization):**
   * **Before:** "We note the caveat plainly: the checkpoint was trained on facts-only inputs, so applying it to facts plus retrieved passages is an inference-time distribution shift, not evidence-aware fine-tuning."
   * **After:** "Because the checkpoint was trained on facts-only inputs, applying it to facts plus retrieved passages is an inference-time distribution shift rather than evidence-aware fine-tuning."
   * **Meaning:** Eliminated formulaic transition wording for direct scholarly prose.
