# Replay directory cleanup map (experiments/audit_fixes/replay/; scan only)

## A. Permanent evidence (KEEP)
bm25.sqlite (rebuilt 2.27GB), bm25_rebuilt.json, bm25_deep_compare.json,
e2_test_predictions.json + repeat, e3e4_replay.json, e1_test1/2.json + e1_test.json +
e1_test_predictions.json, e1/e2 joblib models, leakage_audit.json,
ecourts_corpus_identity.json, e2_cache/ (frozen windows), .db_env (credential, protected)

## B. Final audit reports (KEEP)
paper_claim_audit.md, paper_quantitative_claims.csv, paper_citation_audit.md,
paper_originality_audit.md, paper_issue_list.md, paper_final_verification_matrix.md,
AUDIT_GAPS_UPDATE.md, revision_change_log.md, final_claim_consistency_audit.md,
final_revision_change_log.md, final_reference_resolution.md, 6page_change_log.md,
6page_claim_check.md, audit_fixes_manifest.json

## C. Replay outputs for reproducibility (KEEP)
e2_inference.log, e2_cache_prep.log, e2_repeat2.log, e3e4_direct.log,
e3e4_replay_gpu*.log, pytest.log, fastapi log, spring_retest.log, provenance_load.json

## D/E. Historical + temporary run logs (REVIEW: keep evidence-relevant, drop pure build noise later)
bm25.log, corpus.log, e1.log, e1_1.log, e1_2.log, pytest_fastapi.log, p6*.log,
pip_*.log, free.log, nvidia.log, docker_info.log (0B, BROKEN — recapture or drop),
final*_pass*.log / sixpage*_pass*.log / latex_pass*.log (~60 tex build logs — regenerable),
paper_master_*.aux/.log/.out (regenerable)

## F. One-off scripts
generate_manifest.py (root of replay/) — check vs scripts/generate_manifest2.py output

## G. Duplicate outputs
e2_test_predictions_repeat.json (exact dup of e2_test_predictions.json — intentional match proof, KEEP),
paper_master_original_backup.* (exact dup of master — KEEP as safety),
e2_hf_cache/ (dup of artifacts/e2_hf_cache — keep until replays done)

## H. Intermediate failed-run artifacts
e3e4_replay.log (CUDA failure), e3e4_replay_gpu2.log (rotation race), bm25_verify.log (early),
e2.log (early CUDA failure), bm25_ranking_probe.json (117B vacuous 0-query result — superseded by deep_compare)

## I. Safe-to-regenerate
e2_cache/ (re-runnable via prepare script + DB, slow), spring-api-copy/target/ (mvn package),
paper aux/log/out, tex pass logs

## J. Unknown / needs owner
validation_replay/ role (sibling dup of e2_cache); 6page_change_log.md + 6page_claim_check.md
authorship (another session); audit_fixes_manifest.json vs generate_manifest outputs
