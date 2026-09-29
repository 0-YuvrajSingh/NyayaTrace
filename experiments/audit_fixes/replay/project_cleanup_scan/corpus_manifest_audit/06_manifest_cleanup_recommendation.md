# 06 — cleanup recommendation: KEEP_AUDIT_EVIDENCE
- NOT SAFE_DELETE_AFTER_OWNER_APPROVAL: fails the criteria (unique audit/provenance
  value exists — sole record of executed nested-dup cleanup with per-file SHAs;
  no equivalent authoritative artifact survives; deletion would harm future
  corpus-dup interpretation).
- NOT regenerable safely: sources are gone; only this file lists them.
- BOM defect is cosmetic for audit use (consumers must read utf-8-sig); repair is
  explicitly out of scope and unneeded for its evidence role.
- Owner approval required for ANY future disposition (re-classification, repair, or
  archival). No action taken in this phase.
