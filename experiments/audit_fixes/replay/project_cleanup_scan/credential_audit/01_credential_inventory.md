# 01 — Database Credential Inventory (Read-Only)

## 1. File Identity

- **Exact Path:** `experiments/audit_fixes/replay/.db_env`
- **File Size:** 132 bytes
- **Modification Time (UTC):** `2026-09-28 15:24:25 UTC` (Local: `2026-09-28 20:54:25 +05:30`)
- **SHA-256 Checksum:** `d2cb3b420bb7c758f1b514025a5a097804263b31557ba7d395291c95471141d2`
- **Tracked Status:** Untracked (absent from Git index)
- **Gitignore Status:** Explicitly ignored by rule on line 48 of `.gitignore` (`experiments/audit_fixes/replay/.db_env`)

---

## 2. Configuration & Non-Secret Connection Metadata

- **Target Database:** `legal_xai`
- **Target User:** `legal_xai`
- **Target Host:** `host.docker.internal`
- **Target Port:** `54329`
- **Protocol / Scheme:** `postgresql`
- **Parameter Key:** `LEGAL_XAI_DATABASE_URL`
- **Secret Password:** `[REDACTED]` (length: 48 characters)
- **Sanitized Connection Pattern:** `postgresql://legal_xai:[REDACTED]@host.docker.internal:54329/legal_xai`

---

## 3. Credential Currency Determination

- **Status:** **CURRENT**
- **Verification:**
  - Corresponds directly to the active Docker PostgreSQL container (`legal-xai-postgres`, port `54329:5432`, user `legal_xai`, database `legal_xai`).
  - Generated during Phase 16 password rotation (`experiments/audit_fixes/scripts/rotate_db_password.py`).
  - Successfully verified in audit replay run `gpu3` (`experiments/audit_fixes/replay/logs/e3e4_replay_gpu3.log`).
