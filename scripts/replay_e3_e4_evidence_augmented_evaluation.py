"""Replay E3/E4 only and compare stable output with the frozen 30-case artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def stable_payload(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: stable_payload(item)
            for key, item in value.items()
            if key != "retrieval_run_id"
        }
    if isinstance(value, list):
        return [stable_payload(item) for item in value]
    return value


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--reference",
        type=Path,
        default=ROOT / "artifacts/e3_e4_evidence_augmented_evaluation.json",
    )
    args = parser.parse_args()
    reference = json.loads(args.reference.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="legal-xai-e3e4-replay-") as directory:
        replay_path = Path(directory) / "replay.json"
        environment = os.environ.copy()
        environment["PYTHONPATH"] = os.pathsep.join(
            [str(ROOT / "src"), str(ROOT / "scripts"), environment.get("PYTHONPATH", "")]
        )
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/run_e3_e4_evidence_augmented_evaluation.py"),
                "--output",
                str(replay_path),
                "--force",
            ],
            cwd=ROOT,
            env=environment,
            check=True,
        )
        replay = json.loads(replay_path.read_text(encoding="utf-8"))

    stable_reference = stable_payload(reference)
    stable_replay = stable_payload(replay)
    reference_hash = canonical_sha256(stable_reference)
    replay_hash = canonical_sha256(stable_replay)
    if stable_reference != stable_replay:
        raise RuntimeError(
            f"E3/E4 replay mismatch: reference {reference_hash}, replay {replay_hash}"
        )
    print(
        json.dumps(
            {
                "status": "PASS",
                "population_n": reference["population"]["n"],
                "stable_sha256": reference_hash,
                "excluded_nondeterministic_fields": ["retrieval_run_id"],
                "E3_outcome_prediction": reference["E3_outcome_prediction"],
                "E4_outcome_prediction": reference["E4_outcome_prediction"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
