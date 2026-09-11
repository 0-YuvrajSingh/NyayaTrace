"""Tests for the shared E3/E4 evidence-augmented prediction contract."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from legal_xai.evidence_augmented_prediction import (
    build_evidence_augmented_input,
    mean_logit_prediction,
    window_starts,
)


@dataclass(frozen=True)
class Evidence:
    text: str


def test_input_is_facts_followed_by_selected_passages_in_order() -> None:
    built = build_evidence_augmented_input(
        "  case facts  ",
        [Evidence(" first passage "), Evidence("second passage")],
    )
    assert built == "case facts\n\nfirst passage\n\nsecond passage"


def test_windowing_matches_corrected_e2_full_coverage_rule() -> None:
    starts = window_starts(token_count=1_200, content_size=510, overlap_tokens=50)
    spans = [(start, min(start + 510, 1_200)) for start in starts]
    assert starts == [0, 460, 690]
    assert spans[-1][1] == 1_200
    assert all(next_start <= end for (_, end), (next_start, _) in zip(spans, spans[1:]))


def test_mean_logit_argmax_is_the_only_decision_rule() -> None:
    predicted, pooled = mean_logit_prediction(np.asarray([[4.0, 1.0], [0.0, 5.0]]))
    assert predicted == 1
    np.testing.assert_array_equal(pooled, np.asarray([2.0, 3.0]))


def test_config_reuses_frozen_e2_checkpoint_for_both_experiments() -> None:
    config = json.loads(
        Path("config/e3_e4_evidence_augmented_prediction.json").read_text(encoding="utf-8")
    )
    assert config["experiments"] == ["E3", "E4"]
    assert config["model"]["checkpoint"].endswith("checkpoint-6318")
    assert config["model"]["checkpoint_sha256"] == (
        "924a5bb9078bcc212ef07acb9f08dfaa8593e880ae3868203deb28586dbdc773"
    )
    assert config["input"]["max_length"] == 512
    assert config["input"]["overlap_tokens"] == 50
    assert config["inference"]["seed"] == 202607
    assert config["inference"]["threshold"] is None
    assert config["inference"]["decision_rule"] == "argmax(mean(window_logits, axis=0))"
    assert config["evaluation"]["prediction_delta_canonical"] is False
