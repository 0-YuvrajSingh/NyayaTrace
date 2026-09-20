"""Minimal FastAPI wrapper around the EXISTING NyayaTrace research pipeline.

API wrapper only: no new ML, retrieval, verification, or prediction logic lives
here. Every research step delegates to ``src/legal_xai`` (facts, retrieval,
temporal eligibility, evidence selection, grounded explanation, citation
verification, evidence-augmented prediction) with the frozen ``config/``
versions. Heavy ``legal_xai`` imports are lazy so unit tests can exercise the
HTTP layer with mocked pipeline seams and without torch/sklearn/psycopg.

Endpoints:
  GET  /health          - service + local asset readiness (no inference)
  POST /research/query  - E4 evidence path over caller-supplied facts text
"""

from __future__ import annotations

import json
import os
import re
import sys
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

INDEX_PATH = Path(os.getenv("BM25_INDEX_PATH", str(REPO_ROOT / "retrieval" / "bm25.sqlite")))
DEDUP_MATCHES = Path(os.getenv("DEDUP_MATCHES_PATH", str(REPO_ROOT / "corpus" / "dedup_matches.csv")))
SELECTION_CONFIG = Path(os.getenv("SELECTION_CONFIG_PATH", str(REPO_ROOT / "config" / "evidence_selection.json")))
ANSWER_CONFIG = Path(os.getenv("ANSWER_CONFIG_PATH", str(REPO_ROOT / "config" / "grounded_answer.json")))
PREDICTION_CONFIG = Path(os.getenv("PREDICTION_CONFIG_PATH", str(REPO_ROOT / "config" / "e3_e4_evidence_augmented_prediction.json")))
DATABASE_URL_ENV = "LEGAL_XAI_DATABASE_URL"
INTERNAL_TOKEN_ENV = "ML_INTERNAL_TOKEN"

DEFAULT_QUERY_YEAR = 2020
MAX_CANDIDATE_K = 500
MAX_TOP_K = 10

app = FastAPI(title="NyayaTrace research ML service (local demo)")


class ResearchQuery(BaseModel):
    query: str = Field(min_length=1, description="Facts-only text or legal research question")
    query_id: str = Field(default="demo-query", min_length=1, max_length=128)
    query_year: int = Field(default=DEFAULT_QUERY_YEAR, ge=1900, le=2100)
    candidate_k: int = Field(default=100, ge=1, le=MAX_CANDIDATE_K)
    top_k: int = Field(default=5, ge=1, le=MAX_TOP_K)
    include_prediction: bool = False


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise HTTPException(status_code=503, detail=f"required configuration unavailable: {path.name}") from error
    except json.JSONDecodeError as error:
        raise HTTPException(status_code=500, detail=f"configuration unreadable: {path.name}") from error


def _renderer_version() -> str | None:
    """Read the frozen renderer version without importing heavy pipeline deps.

    Parsing the source keeps the HTTP layer unit-testable without
    torch/sklearn/psycopg while still gating on the single frozen literal.
    """
    try:
        text = (REPO_ROOT / "src" / "legal_xai" / "grounded_answer.py").read_text(encoding="utf-8")
    except OSError:
        return None
    match = re.search(r"^ANSWER_VERSION\s*=\s*[\"']([^\"']+)[\"']", text, re.MULTILINE)
    return match.group(1) if match else None


def _index_version() -> str:
    try:
        if str(SCRIPTS_DIR) not in sys.path:
            sys.path.insert(0, str(SCRIPTS_DIR))
        from build_bm25_index import INDEX_VERSION  # noqa: PLC0415

        return str(INDEX_VERSION)
    except Exception:
        return "fts5-bm25-unicode61-temporal-v2"


def _database_url() -> str:
    url = os.getenv(DATABASE_URL_ENV)
    if url:
        return url
    try:
        if str(SCRIPTS_DIR) not in sys.path:
            sys.path.insert(0, str(SCRIPTS_DIR))
        from load_provenance import DEFAULT_DATABASE_URL  # noqa: PLC0415

        return str(DEFAULT_DATABASE_URL)
    except Exception as error:
        raise HTTPException(status_code=503, detail="provenance database is not configured") from error


def do_retrieve(*, query_id: str, query_year: int, query: str, candidate_k: int,
                selection: dict[str, Any]) -> Any:
    """Run frozen retrieval + diverse selection. Monkeypatched in unit tests."""
    from legal_xai.evidence_pipeline import (  # noqa: PLC0415
        retrieve_temporal_candidates,
        select_diverse_evidence,
    )

    if not INDEX_PATH.exists():
        raise HTTPException(status_code=503, detail="BM25 index is unavailable")
    if candidate_k < 1:
        raise HTTPException(status_code=422, detail="candidate_k must be positive")
    try:
        retrieved = retrieve_temporal_candidates(
            query_id=query_id,
            query_year=query_year,
            query=query,
            candidate_k=candidate_k,
            index_path=INDEX_PATH,
            database_url=_database_url(),
            dedup_matches=DEDUP_MATCHES,
            index_version=f"{_index_version()};{selection['selection_version']}",
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    try:
        selected = select_diverse_evidence(retrieved.candidates, int(selection["max_selected_evidence"]))
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return retrieved, selected


def do_render_verify(*, answer_query: str, selected: Any, run_id: str,
                     query_id: str, query_year: int) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Render the extract-only explanation and fail-closed verify it."""
    from legal_xai.citation_verifier import CorpusEvidenceRecord, verify_answer_citations  # noqa: PLC0415
    from legal_xai.grounded_answer import (  # noqa: PLC0415
        assert_answer_grounded,
        render_grounded_answer,
    )
    from legal_xai.retrieval import query_exclusion_cases  # noqa: PLC0415

    try:
        import psycopg  # noqa: PLC0415
    except ImportError as error:
        raise HTTPException(status_code=503, detail="provenance database driver is unavailable") from error

    try:
        answer = render_grounded_answer(query=answer_query, selected_evidence=selected).as_dict()
        assert_answer_grounded(answer, selected)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    chunk_ids = [item["chunk_id"] for item in answer.get("supporting_evidence", [])]
    records: dict[str, Any] = {}
    retrieved_chunk_ids: set[str] = set()
    try:
        with psycopg.connect(_database_url()) as connection:
            with connection.cursor() as cursor:
                if chunk_ids:
                    cursor.execute(
                        "SELECT chunk_id, source_id, case_id, citation, decision_date, title, court, "
                        "pdf_file, page_number, passage_start_char, passage_end_char, chunk_text "
                        "FROM corpus_chunks WHERE chunk_id = ANY(%s)",
                        (chunk_ids,),
                    )
                    records = {
                        row[0]: CorpusEvidenceRecord(
                            chunk_id=row[0], source_id=row[1], case_id=row[2], citation=row[3],
                            decision_date=row[4].isoformat(), title=row[5], court=row[6],
                            pdf_file=row[7], page_number=row[8], passage_start_char=row[9],
                            passage_end_char=row[10], text=row[11],
                        )
                        for row in cursor.fetchall()
                    }
                cursor.execute(
                    "SELECT chunk_id FROM retrieval_results WHERE run_id = %s AND temporal_status = 'eligible'",
                    (run_id,),
                )
                retrieved_chunk_ids = {row[0] for row in cursor.fetchall()}
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=503, detail="provenance database is unavailable") from error

    checks = verify_answer_citations(
        answer=answer, query_id=query_id, query_year=query_year, corpus_records=records,
        retrieved_chunk_ids=retrieved_chunk_ids,
        audited_near_case_ids=query_exclusion_cases(query_id, DEDUP_MATCHES),
    )
    failed = [check.as_dict() for check in checks if not check.passed]
    if failed:
        raise HTTPException(status_code=422, detail=f"E4 citation verification failed for {len(failed)} citation(s)")
    return answer, [check.as_dict() for check in checks]


def do_predict(*, facts_text: str, selected: Any) -> tuple[dict[str, Any] | None, str | None]:
    """Run the shared frozen E3/E4 predictor; (prediction, skipped_reason)."""
    try:
        from legal_xai.evidence_augmented_prediction import EvidenceAugmentedPredictor  # noqa: PLC0415
    except ImportError:
        return None, "prediction runtime (torch/transformers) is unavailable"
    try:
        predictor = EvidenceAugmentedPredictor.from_config(PREDICTION_CONFIG)
    except (RuntimeError, ValueError) as error:
        return None, str(error)
    except Exception as error:
        return None, f"prediction unavailable: {type(error).__name__}"
    try:
        return predictor.predict(facts_text=facts_text, selected_evidence=selected).as_dict(), None
    except Exception as error:
        return None, f"prediction failed: {type(error).__name__}"


@app.get("/health")
def health() -> dict[str, Any]:
    try:
        selection = _load_json(SELECTION_CONFIG)
        answer_config = _load_json(ANSWER_CONFIG)
        renderer_version = _renderer_version()
        versions_ok = (
            renderer_version is not None
            and answer_config.get("answer_version") == renderer_version
            and answer_config.get("generation_mode") == "controlled_extract_only"
        )
    except HTTPException:
        versions_ok = False
        selection = {}
    try:
        import torch  # noqa: PLC0415

        cuda_available: bool | None = bool(torch.cuda.is_available())
    except ImportError:
        cuda_available = None
    return {
        "status": "ok",
        "index_available": INDEX_PATH.exists(),
        "dedup_available": DEDUP_MATCHES.exists(),
        "selection_version": selection.get("selection_version"),
        "renderer_config_ok": versions_ok,
        "checkpoint_present": (REPO_ROOT / "artifacts" / "e2_chunk_pool_checkpoints_cached"
                               / "checkpoint-6318" / "model.safetensors").exists(),
        "cuda_available": cuda_available,
    }


@app.post("/research/query")
def research_query(body: ResearchQuery, request: Request) -> dict[str, Any]:
    expected = os.getenv(INTERNAL_TOKEN_ENV, "")
    if expected:
        import hmac as _hmac

        presented = request.headers.get("X-Internal-Token", "")
        if not _hmac.compare_digest(presented.encode(), expected.encode()):
            raise HTTPException(status_code=401, detail="unauthorized")
    if body.top_k > body.candidate_k:
        raise HTTPException(status_code=422, detail="candidate_k must be at least top_k")
    selection = _load_json(SELECTION_CONFIG)
    answer_config = _load_json(ANSWER_CONFIG)
    renderer_version = _renderer_version()
    if renderer_version is None:
        raise HTTPException(status_code=503, detail="research pipeline is unavailable")
    if answer_config.get("answer_version") != renderer_version:
        raise HTTPException(status_code=500, detail="grounded-answer configuration mismatch")
    if answer_config.get("generation_mode") != "controlled_extract_only":
        raise HTTPException(status_code=500, detail="extract-only renderer is required")

    request_id = uuid.uuid4().hex
    retrieved, selected = do_retrieve(
        query_id=body.query_id, query_year=body.query_year, query=body.query,
        candidate_k=body.candidate_k, selection=selection,
    )
    selected = tuple(selected)[: body.top_k]
    answer, checks = do_render_verify(
        answer_query=body.query, selected=selected, run_id=retrieved.run_id,
        query_id=body.query_id, query_year=body.query_year,
    )
    prediction: dict[str, Any] | None = None
    prediction_skipped: str | None = None
    if body.include_prediction:
        prediction, prediction_skipped = do_predict(facts_text=body.query, selected_evidence=selected)

    selected_dicts = [item.as_dict() if hasattr(item, "as_dict") else dict(item) for item in selected]
    passed = sum(1 for check in checks if check.get("passed"))
    return {
        "request_id": request_id,
        "experiment": "E4",
        "selection_version": selection.get("selection_version"),
        "query_construction_version": selection.get("query_construction_version"),
        "run_id": retrieved.run_id if hasattr(retrieved, "run_id") else None,
        "query_id": body.query_id,
        "query_year": body.query_year,
        "candidate_count": len(retrieved.candidates) if hasattr(retrieved, "candidates") else 0,
        "selected_evidence_count": len(selected_dicts),
        "query_duplicate_chunks_excluded": getattr(retrieved, "query_duplicate_chunks_excluded", 0),
        "status_counts": dict(retrieved.status_counts) if hasattr(retrieved, "status_counts") else {},
        "legal_issue": answer.get("legal_issue"),
        "applicable_law_and_cases": answer.get("applicable_law_and_cases"),
        "supporting_evidence": answer.get("supporting_evidence"),
        "conclusion": answer.get("conclusion"),
        "evidence_sufficiency": answer.get("evidence_sufficiency"),
        "uncertainty": answer.get("uncertainty"),
        "explanation_order": answer.get("explanation_order"),
        "answer_version": answer.get("answer_version"),
        "provenance": [
            {key: item.get(key) for key in (
                "chunk_id", "source_id", "case_id", "citation", "decision_date", "court",
                "pdf_file", "page_number", "passage_start_char", "passage_end_char",
            )}
            for item in selected_dicts
        ],
        "citation_verification": {
            "status": "passed" if checks and passed == len(checks) else ("empty" if not checks else "failed"),
            "passed_count": passed,
            "checks": checks,
        },
        "outcome_prediction": prediction,
        "prediction_skipped_reason": prediction_skipped,
        "meta": {
            "index_version": _index_version(),
            "answer_version": answer.get("answer_version"),
            "verification_version": "week9-citation-evidence-verifier-v2",
            "temporal_policy": "precedent_decision_year < ildc_query_year; same-year excluded as ambiguous",
        },
    }
