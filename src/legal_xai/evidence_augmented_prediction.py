"""Shared E3/E4 outcome inference using the frozen E2 checkpoint.

The predictor performs inference-time evidence augmentation only. It does not
train or modify the checkpoint. E3 and E4 call the same implementation with
the facts extract followed by the selected verbatim evidence passages.
"""

from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Protocol

import numpy as np
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class EvidenceText(Protocol):
    """Minimum selected-evidence interface needed by the predictor."""

    text: str


def window_starts(token_count: int, content_size: int, overlap_tokens: int) -> list[int]:
    """Return the exact full-coverage window starts used by corrected E2."""

    if content_size < 1:
        raise ValueError("content_size must be positive")
    if not 0 <= overlap_tokens < content_size:
        raise ValueError("overlap_tokens must be non-negative and smaller than content_size")
    if token_count <= content_size:
        return [0]
    starts = list(range(0, token_count - content_size + 1, content_size - overlap_tokens))
    final_start = token_count - content_size
    if starts[-1] != final_start:
        starts.append(final_start)
    return starts


def build_evidence_augmented_input(facts_text: str, selected_evidence: Iterable[EvidenceText]) -> str:
    """Join facts and selected passages without injecting metadata or labels."""

    facts = facts_text.strip()
    if not facts:
        raise ValueError("facts_text must not be empty")
    passages = [item.text.strip() for item in selected_evidence if item.text.strip()]
    return "\n\n".join([facts, *passages])


def mean_logit_prediction(logits: np.ndarray) -> tuple[int, np.ndarray]:
    """Apply E2's primary document-level mean-logit pooling and argmax rule."""

    if logits.ndim != 2 or logits.shape[0] < 1 or logits.shape[1] != 2:
        raise ValueError("logits must have shape (one_or_more_windows, 2)")
    mean_logits = logits.mean(axis=0)
    return int(np.argmax(mean_logits)), mean_logits


def encode_bert_window(tokenizer, token_ids: list[int], max_length: int) -> dict[str, list[int]]:
    """Encode one BERT window equivalently to E2's frozen prepare_for_model call.

    Transformers 5 removed ``BertTokenizer.prepare_for_model``. The explicit
    construction below retains the Transformers 4.46.3 E2 behavior: special
    tokens, right padding, attention mask, and all-zero single-sequence token
    types.
    """

    if tokenizer.cls_token_id is None or tokenizer.sep_token_id is None or tokenizer.pad_token_id is None:
        raise ValueError("frozen BERT tokenizer is missing required CLS, SEP, or PAD token IDs")
    input_ids = [tokenizer.cls_token_id, *token_ids, tokenizer.sep_token_id]
    if len(input_ids) > max_length:
        raise ValueError("window exceeds max_length after adding special tokens")
    token_type_ids = [0] * len(input_ids)
    attention_mask = [1] * len(input_ids)
    padding_length = max_length - len(input_ids)
    if tokenizer.padding_side != "right":
        raise ValueError("frozen E2 encoding requires right padding")
    input_ids += [tokenizer.pad_token_id] * padding_length
    attention_mask += [0] * padding_length
    token_type_ids += [0] * padding_length
    return {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "token_type_ids": token_type_ids,
    }


@dataclass(frozen=True)
class OutcomePrediction:
    config_id: str
    predicted_label: int
    mean_logits: tuple[float, float]
    decision_rule: str
    threshold: None
    input_sha256: str
    input_token_count: int
    window_count: int
    checkpoint: str
    checkpoint_sha256: str
    model_id: str
    model_revision: str
    seed: int

    def as_dict(self) -> dict[str, object]:
        return {
            "config_id": self.config_id,
            "predicted_label": self.predicted_label,
            "mean_logits": list(self.mean_logits),
            "decision_rule": self.decision_rule,
            "threshold": self.threshold,
            "input_sha256": self.input_sha256,
            "input_token_count": self.input_token_count,
            "window_count": self.window_count,
            "checkpoint": self.checkpoint,
            "checkpoint_sha256": self.checkpoint_sha256,
            "model_id": self.model_id,
            "model_revision": self.model_revision,
            "seed": self.seed,
        }


class EvidenceAugmentedPredictor:
    """Reusable, inference-only predictor shared by E3 and E4."""

    def __init__(self, config: dict[str, object], *, root: Path | None = None) -> None:
        self.config = config
        self.root = (root or Path.cwd()).resolve()
        model_config = config["model"]
        input_config = config["input"]
        inference_config = config["inference"]
        if not isinstance(model_config, dict) or not isinstance(input_config, dict) or not isinstance(inference_config, dict):
            raise TypeError("prediction configuration sections must be objects")

        self.config_id = str(config["config_id"])
        self.model_id = str(model_config["id"])
        self.model_revision = str(model_config["revision"])
        self.checkpoint_relative = str(model_config["checkpoint"])
        self.checkpoint_sha256 = str(model_config["checkpoint_sha256"])
        self.checkpoint = self.root / self.checkpoint_relative
        self.max_length = int(input_config["max_length"])
        self.overlap_tokens = int(input_config["overlap_tokens"])
        self.batch_size = int(inference_config["batch_size"])
        self.seed = int(inference_config["seed"])
        self.device = str(inference_config["device"])

        if self.device != "cuda":
            raise ValueError("the frozen E3/E4 prediction configuration requires CUDA, matching E2 inference")
        if not torch.cuda.is_available():
            raise RuntimeError("E3/E4 prediction requires the frozen CUDA inference environment")
        weights = self.checkpoint / "model.safetensors"
        observed_hash = _sha256(weights)
        if observed_hash != self.checkpoint_sha256:
            raise ValueError(
                f"checkpoint hash mismatch: observed {observed_hash}, expected {self.checkpoint_sha256}"
            )

        _set_inference_seed(self.seed)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, revision=self.model_revision)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.checkpoint).cuda().eval()

    @classmethod
    def from_config(cls, path: Path, *, root: Path | None = None) -> "EvidenceAugmentedPredictor":
        return cls(json.loads(path.read_text(encoding="utf-8")), root=root)

    def predict(self, *, facts_text: str, selected_evidence: Iterable[EvidenceText]) -> OutcomePrediction:
        composite = build_evidence_augmented_input(facts_text, selected_evidence)
        token_ids = self.tokenizer(composite, add_special_tokens=False)["input_ids"]
        content_size = self.max_length - self.tokenizer.num_special_tokens_to_add(pair=False)
        starts = window_starts(len(token_ids), content_size, self.overlap_tokens)
        encoded_windows = [
            encode_bert_window(self.tokenizer, token_ids[start : start + content_size], self.max_length)
            for start in starts
        ]

        logits: list[np.ndarray] = []
        with torch.inference_mode():
            for start in range(0, len(encoded_windows), self.batch_size):
                batch_windows = encoded_windows[start : start + self.batch_size]
                batch = {
                    "input_ids": torch.as_tensor(
                        [item["input_ids"] for item in batch_windows], device="cuda", dtype=torch.long
                    ),
                    "attention_mask": torch.as_tensor(
                        [item["attention_mask"] for item in batch_windows], device="cuda", dtype=torch.long
                    ),
                    "token_type_ids": torch.as_tensor(
                        [item.get("token_type_ids", [0] * self.max_length) for item in batch_windows],
                        device="cuda",
                        dtype=torch.long,
                    ),
                }
                with torch.autocast(device_type="cuda", dtype=torch.float16):
                    logits.append(self.model(**batch).logits.float().cpu().numpy())

        predicted_label, mean_logits = mean_logit_prediction(np.concatenate(logits, axis=0))
        return OutcomePrediction(
            config_id=self.config_id,
            predicted_label=predicted_label,
            mean_logits=tuple(round(float(value), 8) for value in mean_logits),
            decision_rule="argmax(mean(window_logits, axis=0))",
            threshold=None,
            input_sha256=hashlib.sha256(composite.encode("utf-8")).hexdigest(),
            input_token_count=len(token_ids),
            window_count=len(starts),
            checkpoint=self.checkpoint_relative.replace("\\", "/"),
            checkpoint_sha256=self.checkpoint_sha256,
            model_id=self.model_id,
            model_revision=self.model_revision,
            seed=self.seed,
        )


def _set_inference_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()
