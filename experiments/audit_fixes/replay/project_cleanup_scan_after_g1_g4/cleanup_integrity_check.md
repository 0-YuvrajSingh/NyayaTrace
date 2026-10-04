# Cleanup integrity check (G1–G4) — PASS

7. Git status delta: identical to pre-state (M .gitignore + same 8 untracked paths;
   all deletions were ignored/untracked, hence git-invisible by design).
8. Canonical manuscript: FADC2392… (tex) / 93EECD93… (pdf) — unchanged.
9. Key hashes/status: retrieval/bm25.sqlite 3187F7… (2,269,376,512); replay/bm25.sqlite
   F2A70B…; checkpoint model.safetensors 924A5BB9… (437,958,648); e2 results D68BE6…;
   config/ 16, src/ 11, corpus/ 39,219, artifacts/ 176 files — all counts unchanged.
   Both manuscript variants present. .db_env present (132B, untouched).
10. Blocked candidates: all unchanged (corpus pairs, 6page, figures, credential, caches,
    BOM manifest, audit history). No status change.
11. Added files: 4 scan-helper scripts only (cleanup_delta/join/rescan/stats) — legitimate.
12. Missing not in G1–G4: NONE (unexpected-removals check empty).
13. Broken references: none — spring-api-copy had zero references (pre-verified);
    target/node_modules regenerable (isolated mvn proof exit 0, byte-identical jar).
    No source/test/config/doc reference pointed at deleted paths.
14. Security: no new secrets (added files are scan scripts); .db_env still protected;
    no literals in compose (variable interpolation only).
15. PASS — cleanup caused no unintended changes. Near-duplicates intact
    (paper variants, script pairs, JSON refits all present in after-inventory).
    demo/spring-api complete (src + pom.xml verified post-delete; target/ proven
    regenerable, not tracked). No source, reproducibility artifact, or audit evidence lost.

STOP. Blocked groups untouched. Next: owner-directed phase only.
