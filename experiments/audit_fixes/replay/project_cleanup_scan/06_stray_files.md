# Stray / temporary files (scan only; no temp patterns matched repo-wide)

- `dummy*.py`, `test.py`, `*.bak`, `*.orig`, `*.swp`, `*.tmp`, `.DS_Store`,
  `Thumbs.db`: NONE FOUND (recursive scan).
- One-off PowerShell scripts: none found as files (commands were inline).
- One-off audit runners (`run_*.sh`, `*_runner*.sh`, `*_runner2.sh`): present in
  experiments/audit_fixes/scripts/ — classified in 07 (temporary-runner vs reusable).
- Copied source trees in replay dirs: `spring-api-copy/` (full demo/spring-api copy
  incl. `target/`), `e2_hf_cache/` (writable HF copy). See 08/09.
- Recent-audit artifacts: `final*_pass*.log`, `sixpage*_pass*.log`, `latex_pass*.log`
  (~60 small build logs), per-variant `.aux/.log/.out`: regenerable, see generated list.
- `.db_env` (132B, ignored): live credential — NOT stray; SECURITY handling, see 17.
- Empty placeholder files: 20 HF hub `.lock`/`.no_exist` files (normal cache behavior)
  + `logs/docker_info.log` (0 bytes, failed capture). See 14.
