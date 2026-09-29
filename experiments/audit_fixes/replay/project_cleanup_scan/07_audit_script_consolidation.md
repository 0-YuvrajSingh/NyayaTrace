# Audit script consolidation (experiments/audit_fixes/scripts/, ~80 files; scan only)

## Keep as permanent tooling (replay-critical, unique)
- e1_canonical_diff.py, leakage_audit.py, verify_e3e4_functional.py, diff_e3e4.py,
  diagnose_e3e4.py, bm25_deep_compare2.py + runner2.sh, verify_db_env.py,
  rotate_db_password.py, run_pytest.sh, run_fastapi_tests.sh, run_e3e4_replay.sh,
  run_e3e4_direct.sh, run_e2_repeat2.sh, paper_stats/final_stats/final_pages.py,
  cleanup_scan.py, cleanup_join.py, cleanup_stats.py, diff_final.py

## Superseded (newer version exists; keep newer, review older)
- bm25_deep_compare.py/runner.sh → superseded by deep_compare2
- run_e2_repeat.sh → superseded by run_e2_repeat2.sh
- generate_manifest.py → generate_manifest2.py (verify which output is canonical)
- c6_check.py → c6_check2.py; runner_p5.sh → runner_p5_fast.sh (verify)
- compare_bm25.py (early 0-query probe) → superseded by deep_compare2
- bm25_ranking_probe.py + bm25_verify.sh: early probe (vacuous 0-query bug); historical

## Rebuild history (final + sixpage batch scripts, ~20 files)
- rebuild_final_batch{1,2,A,C,D1–D5,E,F,G,R}.py, sixpage_batch{1–7}.py:
  single-use migration scripts. Reusable only as change history. CONSOLIDATE_LATER
  (squash into one documented rebuild log or archive).

## Small probes / getters (keep-or-archive, cheap)
- check_e1.py, get_14_cases.py, get_failed_cases.py, get_verified_on.py, p5_query.py,
  p6_search.py, print_metrics.py, parse_replay.py, c_analysis.py, c9_search.py,
  check_git_drift.py, check_timestamps.py, compare_freeze_hashes.py, count_freeze.py,
  hash_freeze_files.py, freeze_reconciliation.py, paper_evidence_check.py,
  paper_join_check.py, extract_spec.py, clean_spec.py, write_quotes.py,
  answer_key_temporal_check.py, load_provenance_ro.sh, run_d14_d15.sh, p6*.sh/py

## Redundant candidates (verify content before any action)
- e1_1.log/e1_2.log pattern analogues in scripts: none (those are replay outputs).
- final_stats.py vs revised_stats.py vs paper_stats.py vs sixpage_stats.py:
  near-identical page counters → CONSOLIDATE_LATER into one.
- bm25_deep_compare_runner.sh vs runner2.sh: keep runner2 only.

No script deleted. Exact-duplicate check across scripts/: covered by 04 groups
(42 groups under experiments/audit_fixes — mostly tiny identical outputs, recheck per-group).
