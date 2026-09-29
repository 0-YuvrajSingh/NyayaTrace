# Manuscript resolution report (read-only; nothing changed)

## 1. Files
master tex 55,994B (tracked, HEAD) / pdf 293,984B 10pp; revised tex 56,898B / pdf
294,801B 11pp; final tex 37,222B / pdf 204,518B 6pp/4,516w (FADC2392…);
6page tex 31,746B / pdf 222,823B 6pp/3,720w; docx 27,166B (old spec).
Backups: replay/paper_master_original_backup.* (exact master dups).
Build byproducts for revised/final/6page in replay/ (regenerable).
All four share identical section structure (14 sections).

## 2. Pairwise similarity (difflib, tex lines)
master–revised 0.98; master–final 0.53; master–6page 0.50;
revised–final 0.55; revised–6page 0.51; final–6page 0.72.

## 3. Canonical candidate (objective criteria only)
paper_master_final: latest audited version; all 11 revision corrections present;
Base-30 verified core; combined/extension/LLM material artifact-labeled or removed;
6 pages (in range); compiles clean (no errors, no undefined refs, no overflows).
Unresolved: owner submission sign-off (recorded separately).
Candidate: paper_master_final | evidence above | unresolved: formal sign-off only.

## 4. 6page discrepancies (reintroduces removed claims)
- 185/185 combined central ×2 (unlabeled), 56/56 LLM ×2, positive-control 37/37 ×1,
  combined E3/E4 0.648649 ×3, 12/37 ×3, IEEEtrigger lines ×2 (layout hack),
  18pt/37pt overflows (unfixed identifiers), uses combined-data fig2/fig3.
- No byte-identical-E3/E4 or no-leakage-whatsoever claims in any variant.
- 6page build: 0 errors but overflows + trigger lines retained.

## 5. PDF/LaTeX consistency
final: 6pp, clean (verified 2026-09-29). 6page: recompiled 2026-09-29 into scan dir:
0 errors, same 2 overflows, trigger lines present. master/revised PDFs are historical builds.

## 6. Owner decision table
| File | Role | Status | Recommended disposition | Owner decision required |
| --- | --- | --- | --- | --- |
| paper_master_final.* | submission candidate | audited, 6pp, clean | KEEP_AS_CANONICAL | sign-off |
| paper_master.tex/.pdf | tracked baseline | HEAD-committed | KEEP_AS_AUDIT_RECORD | none |
| paper_master_revised.* | previous revision | superseded by final | ARCHIVE | approve archival |
| paper_master_6page.* | alternate variant | reintroduces removed claims | DELETE_AFTER_APPROVAL | approve deletion |
| Indian_Legal_XAI.docx | old spec | obsolete | ARCHIVE | approve archival |
| replay/paper_master_original_backup.* | safety backup | exact master dup | ARCHIVE | approve archival |
| replay paper aux/log/out | build byproducts | regenerable | DELETE_AFTER_APPROVAL | none (regen proof done) |

No disposition executed.

## 7. Figure source check
final references zero figures. master/revised reference figures/fig1–5;
6page references figures/fig2–3 (0.58 width). artifacts/figures/*.pdf are exact
dups, unreferenced by any tex. figures/ must be kept while master/revised/6page
exist; artifacts/figures/ needs no audit-evidence role beyond duplication.
