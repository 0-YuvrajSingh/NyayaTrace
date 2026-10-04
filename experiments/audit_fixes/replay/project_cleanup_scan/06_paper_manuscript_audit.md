# Paper / manuscript audit (scan only)

| paper file | status | pages/words | hash (prefix) | likely role |
| --- | --- | --- | --- | --- |
| paper_master.tex (root, tracked) | TRACKED_BASELINE | 10pp/7,077w (built PDF) | 9DE053A7 | last committed manuscript (HEAD f3ace8a) |
| paper_master.pdf (root, tracked?) | GENERATED_OUTPUT | 10pp | 3B35C279 | committed build of master |
| paper_master_revised.tex/.pdf (untracked) | PREVIOUS_REVISION | 11pp/7,204w | CCFF15E6 | factual-correction pass (this session) |
| paper_master_final.tex/.pdf (untracked) | REVIEW_REQUIRED | 6pp/4,516w | — | Base-30-restructured 6-page candidate (this session) |
| paper_master_6page.tex/.pdf (untracked) | REVIEW_REQUIRED | 6pp/3,720w | — | parallel 6-page variant (another session, 00:10–00:18) |
| Indian_Legal_XAI.docx (tracked?) | OBSOLETE_CANDIDATE | spec draft | 10493242 | older spec, keep as history |
| figures/fig1–5.pdf | KEEP (referenced by master/revised) | — | — | figure sources; final/6page use none |
| artifacts/figures/*.pdf | DUPLICATE_CANDIDATE | — | exact dups of figures/ | frozen copies |
| submission/final/ | UNKNOWN | — | — | resynced per HEAD commit; verify which tex it mirrors |
| replay/paper_master_*.aux/.log/.out | GENERATED_REGENERABLE | — | — | latex build byproducts |
| replay/paper_master_original_backup.* | BACKUP | — | exact dup of master expected | safety copies |

Submission intent: RESOLVED 2026-09-29 — owner decision: paper_master_final is canonical.
CURRENT_CANONICAL: paper_master_final.tex/.pdf (6pp, 4,516w).
paper_master_6page.* retained untouched pending explicit archival decision (REVIEW_REQUIRED).
