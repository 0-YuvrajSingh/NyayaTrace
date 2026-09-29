# Cleanup recommendation (one class per cache; no deletion performed)

| cache | classification | rationale |
| --- | --- | --- |
| replay/e2_cache/ | KEEP_REQUIRED_FOR_REPRODUCTION | cache of record for the verified E2 exact reproductions; actively mounted by replay commands |
| artifacts/e2_hf_cache/ | KEEP_REQUIRED_FOR_REPRODUCTION | frozen read-only hub-asset source; only pristine blob set |
| artifacts/.../checkpoint-6318/ | KEEP_REQUIRED_FOR_REPRODUCTION (implicit) | non-regenerable without retraining; frozen |
| replay/e2_hf_cache/ | REGENERABLE_BUT_UNSAFE_TO_DELETE_YET | derived working copy; safe only after all GPU replays conclude + owner approval |
| validation_replay/ (whole tree) | BLOCKED_PROVENANCE_UNCLEAR | prior independent replay w/ own evidence files; zero active references, but historical research provenance + possible predictions-evidence value; needs owner decision, not filename-based deletion |

Nothing classified SAFE_DELETE_AFTER_OWNER_APPROVAL in this phase: the two plausible
deletion targets (replay HF working copy, validation_replay tree) both fail the safety
bar (active-or-recent runtime role; unresolved historical provenance respectively).
