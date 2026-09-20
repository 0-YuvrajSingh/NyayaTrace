/** Typed mirrors of the demo-stack research envelope (Spring passes through the FastAPI schema). */

export interface AuthorityCard {
  evidence_id: string;
  case_id?: string | null;
  citation?: string | null;
  decision_date?: string | null;
  court?: string | null;
}

export interface EvidenceItem {
  evidence_id: string;
  chunk_id: string;
  source_id: string;
  case_id?: string | null;
  citation?: string | null;
  decision_date?: string | null;
  court?: string | null;
  pdf_file?: string | null;
  page_number?: number | null;
  passage_start_char?: number | null;
  passage_end_char?: number | null;
  verbatim_passage?: string | null;
}

export interface CitationCheck {
  evidence_id?: string | null;
  chunk_id?: string | null;
  citation?: string | null;
  passed: boolean;
  failures: string[];
}

export interface ResearchResult {
  request_id?: string | null;
  experiment?: string | null;
  selection_version?: string | null;
  run_id?: string | null;
  query_id?: string | null;
  query_year?: number | null;
  candidate_count?: number | null;
  selected_evidence_count?: number | null;
  legal_issue?: { text?: string | null } | null;
  applicable_law_and_cases?: AuthorityCard[] | null;
  supporting_evidence?: EvidenceItem[] | null;
  conclusion?: { text?: string | null; mode?: string | null } | null;
  evidence_sufficiency?: string | null;
  uncertainty?: string | null;
  provenance?: Array<Record<string, unknown>> | null;
  citation_verification?: { status?: string | null; passed_count?: number | null; checks?: CitationCheck[] | null } | null;
  outcome_prediction?: { predicted_label?: number | null } | null;
  prediction_skipped_reason?: string | null;
  meta?: Record<string, unknown> | null;
}

export interface ResearchEnvelope {
  request_id: string;
  result: ResearchResult;
}

export interface ExperimentMeta {
  id: string;
  name: string;
  purpose: string;
  status: string;
  population?: string;
}
