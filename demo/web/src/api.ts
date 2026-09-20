import type { ExperimentMeta, ResearchEnvelope, ResearchResult } from './types';

async function request(path: string, token: string | null, init?: RequestInit): Promise<Response> {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  const response = await fetch(path, { ...init, headers: { ...headers, ...(init?.headers ?? {}) } });
  if (response.status === 401) {
    throw new Error('Unauthorized: set the local demo API token.');
  }
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Request failed (${response.status}): ${text.slice(0, 300)}`);
  }
  return response;
}

export async function submitResearch(
  token: string,
  body: { query: string; query_id?: string; query_year?: number; candidate_k?: number; top_k?: number; include_prediction?: boolean },
): Promise<ResearchEnvelope> {
  const response = await request('/api/research/query', token, {
    method: 'POST',
    body: JSON.stringify(body),
  });
  return (await response.json()) as ResearchEnvelope;
}

export async function fetchExperiments(token: string): Promise<ExperimentMeta[]> {
  const response = await request('/api/experiments', token);
  const data = (await response.json()) as { experiments: ExperimentMeta[] };
  return data.experiments ?? [];
}

export async function fetchAudit(token: string, requestId: string): Promise<unknown> {
  const response = await request(`/api/audit/${encodeURIComponent(requestId)}`, token);
  return await response.json();
}

export function isStructuredResult(result: ResearchResult | undefined): result is ResearchResult {
  return !!result && Array.isArray(result.supporting_evidence);
}
