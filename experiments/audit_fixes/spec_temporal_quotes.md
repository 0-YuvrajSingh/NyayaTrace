# Spec Quotes for Temporal Rule

## Operational Definitions Section
[PARAGRAPH] Operational Definitions
[PARAGRAPH] The following definitions formalize concepts already required elsewhere in this document (Temporal Integrity Protocol, Citation and Provenance Protocol, Evaluation Metrics). They clarify measurement so the project does not move its rules after seeing results; they introduce no new technical requirement.
[TABLE] Term | Operational definition
[TABLE] Temporal existence | An authority/document is available in the corpus at or before the relevant historical time.
[TABLE] Temporal effectiveness | A statute/provision is treated as effective only during its defined validity interval when reliable metadata is available.
[TABLE] Temporal applicability | Whether the frozen historical-eligibility rule (Eligible(e,t)) permits the item for the evaluation case.
[TABLE] Provenance validity | The final citation maps to an identified source document and exact passage that was retrieved for the case/query. This is the same quantity already named “Citation Provenance Validity” in the Evaluation Metrics table below.
[TABLE] Authority consistency | The cited authority matches the predefined reference evidence/authority mapping used for evaluation. This is the same quantity already measured by “Authority-consistent Precision/Recall/F1” below.
[PARAGRAPH] These definitions must be frozen before final test evaluation and may not be changed after inspecting results.
[PARAGRAPH] Final Scope

## Temporal Integrity Protocol Section
[PARAGRAPH] Temporal Integrity Protocol
[PARAGRAPH] Temporal eligibility is included as an integrity control for historical evaluation, not as the primary novelty claim. A historical case should not be evaluated using later legal information when the experimental question is what the system could have used at the case decision time.
[PARAGRAPH] Statute passages should carry effective and end-validity metadata where available.
[PARAGRAPH] Precedent eligibility should require decision_date <= case_date, with the target case and duplicates/near-duplicates excluded.
[PARAGRAPH] Unresolved temporal metadata must follow a predefined rule and must not be manually corrected after observing test results.
[PARAGRAPH] Current-law deployment is conceptually different from historical prediction and is not a separate semester benchmark.

## All Keyword Matches in Document
- **Section:** Executive Summary
  **Origin:** [PARAGRAPH] The project will use Indian legal cases and associated authority information, with ILDC as the principal academic benchmark where applicable. The system will combine a traditional benchmark, a legal-language baseline, BM25 retrieval, evidence selection, citation/provenance tracking, a controlled generation layer where feasible, and a structured explanation surface. Temporal eligibility of legal evidence will be implemented as a reliability constraint for historical evaluation, but it is not the primary novelty claim. Multilingual support is explicitly deferred to future work.

- **Section:** Research Gap
  **Origin:** [PARAGRAPH] The proposed project does not claim novelty for Legal-BERT, BM25, RAG, court judgment prediction, or explainability individually. The research gap targeted here is the integration and controlled evaluation of multiple reliability constraints in an Indian legal research workflow: evidence grounding, citation/provenance restriction, temporal eligibility for historical evaluation, and a legally meaningful explanation surface.

- **Section:** Research Objectives
  **Origin:** [PARAGRAPH] Implement temporal eligibility as a historical-evaluation integrity constraint so later legal information does not enter historical test cases.

- **Section:** Research Objectives
  **Origin:** [PARAGRAPH] Evaluate retrieval quality, citation correctness, provenance, temporal integrity, explanation quality, and secondary outcome-prediction performance.

- **Section:** Operational Definitions
  **Origin:** [PARAGRAPH] The following definitions formalize concepts already required elsewhere in this document (Temporal Integrity Protocol, Citation and Provenance Protocol, Evaluation Metrics). They clarify measurement so the project does not move its rules after seeing results; they introduce no new technical requirement.

- **Section:** Operational Definitions
  **Origin:** [TABLE] Temporal existence | An authority/document is available in the corpus at or before the relevant historical time.

- **Section:** Operational Definitions
  **Origin:** [TABLE] Temporal effectiveness | A statute/provision is treated as effective only during its defined validity interval when reliable metadata is available.

- **Section:** Operational Definitions
  **Origin:** [TABLE] Temporal applicability | Whether the frozen historical-eligibility rule (Eligible(e,t)) permits the item for the evaluation case.

- **Section:** Operational Definitions
  **Origin:** [TABLE] Authority consistency | The cited authority matches the predefined reference evidence/authority mapping used for evaluation. This is the same quantity already measured by “Authority-consistent Precision/Recall/F1” below.

- **Section:** Final Scope
  **Origin:** [TABLE] Reliability | Citation verification, provenance, temporal eligibility, audit logging | Automatic certification of substantive legal correctness

- **Section:** OUTPUT
  **Origin:** Temporal Eligibility (historical evaluation)

- **Section:** USER QUERY / CASE FACTS
  **Origin:** TEMPORAL ELIGIBILITY

- **Section:** E1–E4 Experimental Core
  **Origin:** [TABLE] E4 — Proposed Explainable Framework | E3 + provenance-constrained selection + citation validation + structured explanation + temporal integrity | Case facts/query + selected evidence + provenance metadata | Test whether reliability and explainability constraints improve evidence quality and transparency without unacceptable performance loss.

- **Section:** E1–E4 Experimental Core
  **Origin:** [PARAGRAPH] E3 and E4 must use the same data splits, preprocessing, retrieval index, top-k, model configuration, and random seeds wherever applicable. The controlled change is the evidence-control, verification, temporal-integrity, and explanation layer.

- **Section:** Temporal Integrity Protocol
  **Origin:** [PARAGRAPH] Temporal Integrity Protocol

- **Section:** Temporal Integrity Protocol
  **Origin:** [PARAGRAPH] Temporal eligibility is included as an integrity control for historical evaluation, not as the primary novelty claim. A historical case should not be evaluated using later legal information when the experimental question is what the system could have used at the case decision time.

- **Section:** Temporal Integrity Protocol
  **Origin:** [PARAGRAPH] Precedent eligibility should require decision_date <= case_date, with the target case and duplicates/near-duplicates excluded.

- **Section:** Temporal Integrity Protocol
  **Origin:** [PARAGRAPH] Unresolved temporal metadata must follow a predefined rule and must not be manually corrected after observing test results.

- **Section:** FINAL CITATION
  **Origin:** TEMPORAL ELIGIBILITY CHECK

- **Section:** FINAL CITATION
  **Origin:** [PARAGRAPH] Minimum stored fields: source_id, source_type, authority_name, citation_or_section, passage_id, retrieval_rank, date, temporal_eligibility, and case/query identifier.

- **Section:** Evaluation Metrics
  **Origin:** [TABLE] Citation | Authority-consistent Precision / Recall / F1 | Whether cited authorities match the predefined evaluation evidence

- **Section:** Evaluation Metrics
  **Origin:** [TABLE] Integrity | Temporal Violation Rate | Frequency of temporally ineligible evidence entering historical output

- **Section:** Evaluation Metrics
  **Origin:** [PARAGRAPH] Note on scope: Temporal Violation Rate is the sole required temporal integrity metric. Named sub-decompositions (e.g., separately reporting retrieved-set exposure versus final-citation exposure, or a prediction delta across E3/E4) were reviewed and are explicitly not adopted as additional required metrics, since they are not part of the approved baseline. Nothing prevents the implementation team from computing such breakdowns internally for debugging, but they must not be reported as frozen evaluation deliverables or used to imply a broader evaluation objective than the one specified here.

- **Section:** Evaluation Reference Evidence
  **Origin:** [PARAGRAPH] Retrieval and citation evaluation must use a predefined reference evidence set or defensible authority mapping available before final test evaluation. The reference must not be constructed retrospectively from the system’s own retrieved output. If existing ILDC authority/explanation annotations are used, the mapping procedure must be documented and frozen before final scoring. [2]

- **Section:** Mandatory Error Analysis
  **Origin:** [PARAGRAPH] Citation is later than the historical case date: temporal integrity failure.

- **Section:** Temporal eligibility implementation
  **Origin:** [PARAGRAPH] Temporal eligibility implementation

- **Section:** 14–16 Week Timeline
  **Origin:** [TABLE] 3–4 | Corpus preprocessing; metadata normalization; passage segmentation; BM25 index; temporal metadata; provenance schema. | Stable corpus + retrieval smoke test

- **Section:** 14–16 Week Timeline
  **Origin:** [TABLE] 9–10 | Implement E4 provenance constraints, citation verification, temporal checks, and structured explanation. | Proposed explainable framework

- **Section:** 14–16 Week Timeline
  **Origin:** [TABLE] 11–12 | Full evaluation; citation/grounding metrics; temporal integrity metrics; secondary prediction metrics; mandatory error analysis. | Final experiment tables

- **Section:** Citation, Provenance, and Temporal Integrity
  **Origin:** [PARAGRAPH] Citation, Provenance, and Temporal Integrity

- **Section:** Limitations
  **Origin:** [PARAGRAPH] Temporal eligibility is an experimental integrity rule, not a universal statement of legal applicability.

- **Section:** Future Work
  **Origin:** [PARAGRAPH] Conflicting-precedent detection and temporal evolution graphs.

- **Section:** Final One-Paragraph Summary
  **Origin:** [PARAGRAPH] This project proposes an Explainable AI Framework for Indian legal research in which a legal question or historical case is processed through a legal-language model and an explicit legal retrieval pipeline. BM25 retrieves relevant statutes and precedent passages; an evidence-selection layer chooses support; provenance metadata records the exact source and passage; citation validation rejects unsupported authorities; temporal eligibility prevents later information from entering historical evaluation; and an explanation layer exposes the evidence basis of the final output. The core evaluation compares a traditional predictive baseline, a facts-only legal-language baseline, a retrieval-grounded legal research system, and the full provenance-constrained explainable framework using retrieval, citation, grounding, temporal-integrity, provenance, explanation, and secondary outcome-prediction metrics. The project does not attempt to replace judges or lawyers, and multilingual support is intentionally deferred to future work.

