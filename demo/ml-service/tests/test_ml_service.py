"""Unit tests for the FastAPI demo wrapper.

Heavy research execution (BM25/PostgreSQL/torch) is monkeypatched at the
module seams (``do_retrieve``/``do_render_verify``/``do_predict``), so these
tests run without model weights, index, or database. They verify the HTTP
contract, output schema, error mapping, and end-to-end wiring only.
"""

from fastapi.testclient import TestClient

import app as ml_app


class _Retrieved:
    def __init__(self):
        self.run_id = "00000000-0000-4000-8000-000000000001"
        self.query_id = "week10-replay-01"
        self.query_year = 2020
        self.candidates = [{"chunk_id": f"c{i}"} for i in range(100)]
        self.query_duplicate_chunks_excluded = 0
        self.status_counts = {"eligible": 100}


def _candidate(chunk_id="S_2000_1_1_1::p0001::c001"):
    return {
        "rank": 1,
        "chunk_id": chunk_id,
        "source_id": "S_2000_1_1_1",
        "case_id": "2000 INSC 1",
        "citation": "[2000] 1 S.C.R. 1",
        "decision_date": "2000-01-01",
        "court": "Supreme Court of India",
        "pdf_file": "S_2000_1_1_1_EN.pdf",
        "page_number": 1,
        "passage_start_char": 0,
        "passage_end_char": 10,
        "bm25_score": 10.0,
        "temporal_status": "eligible",
        "text": "verbatim passage",
    }


class _Selected:
    def __init__(self, payload):
        self._payload = payload

    def as_dict(self):
        return dict(self._payload)


ANSWER = {
    "answer_version": "week10-verified-explanation-renderer-v1",
    "explanation_order": ["legal_issue", "applicable_law_and_cases", "supporting_evidence",
                          "conclusion", "uncertainty"],
    "legal_issue": {"text": "anticipatory bail section 438", "source": "user_query"},
    "applicable_law_and_cases": [{"evidence_id": "E1", "case_id": "2000 INSC 1",
                                  "citation": "[2000] 1 S.C.R. 1",
                                  "decision_date": "2000-01-01",
                                  "court": "Supreme Court of India"}],
    "supporting_evidence": [{
        "evidence_id": "E1", "chunk_id": "S_2000_1_1_1::p0001::c001",
        "source_id": "S_2000_1_1_1", "case_id": "2000 INSC 1",
        "citation": "[2000] 1 S.C.R. 1", "decision_date": "2000-01-01",
        "court": "Supreme Court of India", "pdf_file": "S_2000_1_1_1_EN.pdf",
        "page_number": 1, "passage_start_char": 0, "passage_end_char": 10,
        "verbatim_passage": "verbatim passage"}],
    "conclusion": {"text": "No legal conclusion is inferred beyond the cited supporting evidence.",
                   "mode": "evidence_bound_no_inference", "evidence_ids": ["E1"]},
    "evidence_sufficiency": "limited",
    "uncertainty": "This is an evidence-grounded research brief, not legal advice. "
                   "It reports only the selected retrieved passages and does not infer "
                   "conclusions beyond them. Missing or incomplete evidence should be "
                   "reviewed by a human.",
}

CHECKS = [{"evidence_id": "E1", "chunk_id": "S_2000_1_1_1::p0001::c001",
           "citation": "[2000] 1 S.C.R. 1", "passed": True, "failures": []}]

client = TestClient(ml_app.app)


def _patch(monkeypatch):
    monkeypatch.setattr(ml_app, "do_retrieve",
                        lambda **kw: (_Retrieved(), [_Selected(_candidate())]))
    monkeypatch.setattr(ml_app, "do_render_verify",
                        lambda **kw: (ANSWER, CHECKS))
    monkeypatch.setattr(ml_app, "do_predict",
                        lambda **kw: ({"predicted_label": 1}, None))


def test_health_shape():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    for key in ("index_available", "dedup_available", "selection_version",
                "renderer_config_ok", "checkpoint_present", "cuda_available"):
        assert key in body


def test_valid_request_wires_seams(monkeypatch):
    _patch(monkeypatch)
    response = client.post("/research/query", json={
        "query": "anticipatory bail section 438",
        "query_id": "week10-replay-01",
        "query_year": 2020,
        "include_prediction": True,
    })
    assert response.status_code == 200
    body = response.json()
    assert body["experiment"] == "E4"
    assert body["query_id"] == "week10-replay-01"
    assert body["request_id"]
    assert body["run_id"] == "00000000-0000-4000-8000-000000000001"
    assert body["citation_verification"]["status"] == "passed"
    assert body["outcome_prediction"] == {"predicted_label": 1}


def test_malformed_requests_rejected(monkeypatch):
    _patch(monkeypatch)
    assert client.post("/research/query", json={"query": ""}).status_code == 422
    assert client.post("/research/query", json={}).status_code == 422
    assert client.post("/research/query",
                       json={"query": "x", "top_k": 5, "candidate_k": 2}).status_code == 422


def test_output_contract_schema(monkeypatch):
    _patch(monkeypatch)
    body = client.post("/research/query",
                       json={"query": "anticipatory bail section 438"}).json()
    for key in ("legal_issue", "applicable_law_and_cases", "supporting_evidence",
                "conclusion", "evidence_sufficiency", "uncertainty",
                "provenance", "citation_verification", "meta"):
        assert key in body, key
    assert "not legal advice" in body["uncertainty"]
    assert "reviewed by a human" in body["uncertainty"]
    assert body["meta"]["temporal_policy"].startswith("precedent_decision_year")
    prov = body["provenance"][0]
    for key in ("chunk_id", "source_id", "citation", "decision_date", "court",
                "pdf_file", "page_number", "passage_start_char", "passage_end_char"):
        assert key in prov, key


def test_smoke_week10_frozen_case_shape(monkeypatch):
    """End-to-end wiring smoke on the frozen week-10 replay query shape."""
    _patch(monkeypatch)
    body = client.post("/research/query", json={
        "query": "anticipatory bail section 438",
        "query_id": "week10-replay-01",
        "query_year": 2020,
        "candidate_k": 100,
        "top_k": 5,
    }).json()
    assert body["candidate_count"] == 100
    assert body["selected_evidence_count"] == 1
    assert body["citation_verification"]["passed_count"] == 1
    raw = client.post("/research/query", json={
        "query": "anticipatory bail section 438"}).content.decode()
    assert "LEGAL_XAI_DATABASE_URL" not in raw
    assert "POSTGRES_PASSWORD" not in raw


def test_pipeline_failure_maps_without_500(monkeypatch):
    from fastapi import HTTPException

    def _fail(**kw):
        raise HTTPException(status_code=422, detail="BM25 returned no candidates")

    monkeypatch.setattr(ml_app, "do_retrieve", _fail)
    response = client.post("/research/query", json={"query": "zzzz qqqq"})
    assert response.status_code == 422
    assert "no candidates" in response.json()["detail"]
