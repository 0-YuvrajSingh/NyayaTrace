import React, { useState } from 'react';
import { fetchAudit, fetchExperiments, submitResearch } from './api';
import type { ExperimentMeta, ResearchEnvelope } from './types';

const DEFAULT_QUERY = 'anticipatory bail section 438';

export default function App(): JSX.Element {
  const [token, setToken] = useState('');
  const [query, setQuery] = useState(DEFAULT_QUERY);
  const [queryId, setQueryId] = useState('week10-replay-01');
  const [queryYear, setQueryYear] = useState('2020');
  const [includePrediction, setIncludePrediction] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [envelope, setEnvelope] = useState<ResearchEnvelope | null>(null);
  const [experiments, setExperiments] = useState<ExperimentMeta[] | null>(null);
  const [audit, setAudit] = useState<unknown>(null);

  async function onSubmit(event: React.FormEvent): Promise<void> {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setEnvelope(null);
    setAudit(null);
    try {
      const result = await submitResearch(token.trim(), {
        query,
        query_id: queryId.trim() || undefined,
        query_year: queryYear.trim() === '' ? undefined : Number(queryYear),
        include_prediction: includePrediction,
      });
      setEnvelope(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Request failed');
    } finally {
      setLoading(false);
    }
  }

  async function onLoadExperiments(): Promise<void> {
    setError(null);
    try {
      setExperiments(await fetchExperiments(token.trim()));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Request failed');
    }
  }

  async function onLoadAudit(): Promise<void> {
    if (!envelope) {
      return;
    }
    setError(null);
    try {
      setAudit(await fetchAudit(token.trim(), envelope.request_id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Request failed');
    }
  }

  const result = envelope?.result;

  return (
    <main>
      <header>
        <h1>NyayaTrace — local research demo</h1>
        <p className="notice">
          AI assistance for legal research only. This is <strong>not legal advice</strong>, and every
          output requires <strong>human verification</strong> against the cited sources.
        </p>
      </header>

      <section aria-label="authentication">
        <h2>1. Local API token</h2>
        <input
          type="password"
          aria-label="demo API token"
          placeholder="DEMO_API_TOKEN value"
          value={token}
          onChange={(event) => setToken(event.target.value)}
        />
      </section>

      <section aria-label="research query">
        <h2>2. Historical case input</h2>
        <form onSubmit={onSubmit}>
          <label>
            Facts / research question
            <textarea rows={5} value={query} onChange={(event) => setQuery(event.target.value)} required />
          </label>
          <div className="row">
            <label>
              Case ID (optional)
              <input value={queryId} onChange={(event) => setQueryId(event.target.value)} />
            </label>
            <label>
              Query year
              <input value={queryYear} onChange={(event) => setQueryYear(event.target.value)} inputMode="numeric" />
            </label>
            <label className="check">
              <input
                type="checkbox"
                checked={includePrediction}
                onChange={(event) => setIncludePrediction(event.target.checked)}
              />
              Include experimental outcome prediction (needs GPU + checkpoint)
            </label>
          </div>
          <button type="submit" disabled={loading || query.trim() === ''}>
            {loading ? 'Researching…' : 'Submit research request'}
          </button>
        </form>
      </section>

      {error && (
        <section aria-label="error" className="error">
          <h2>Error</h2>
          <p>{error}</p>
        </section>
      )}

      {result && (
        <section aria-label="structured result">
          <h2>3. Structured result</h2>
          <dl className="meta">
            <dt>Request</dt>
            <dd>{envelope?.request_id}</dd>
            <dt>Experiment path</dt>
            <dd>{result.experiment ?? '—'}</dd>
            <dt>Retrieval run</dt>
            <dd>{result.run_id ?? '—'}</dd>
            <dt>Candidates / selected</dt>
            <dd>
              {result.candidate_count ?? '—'} / {result.selected_evidence_count ?? '—'}
            </dd>
            <dt>Citation verification</dt>
            <dd>
              {result.citation_verification?.status ?? '—'} (
              {result.citation_verification?.passed_count ?? 0} checks passed)
            </dd>
          </dl>

          <h3>Issue</h3>
          <p>{result.legal_issue?.text ?? '—'}</p>

          <h3>Authorities</h3>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Citation</th>
                <th>Court</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {(result.applicable_law_and_cases ?? []).map((authority) => (
                <tr key={authority.evidence_id}>
                  <td>{authority.evidence_id}</td>
                  <td>{authority.citation ?? '—'}</td>
                  <td>{authority.court ?? '—'}</td>
                  <td>{authority.decision_date ?? '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <h3>Evidence</h3>
          {(result.supporting_evidence ?? []).map((item) => (
            <article key={item.evidence_id} className="evidence">
              <h4>
                {item.evidence_id} — {item.citation ?? 'no citation'} ({item.decision_date ?? 'no date'})
              </h4>
              <blockquote>{item.verbatim_passage ?? ''}</blockquote>
              <p className="provenance">
                {item.source_id} · {item.pdf_file ?? ''} p.{item.page_number ?? '—'} chars{' '}
                {item.passage_start_char ?? '—'}–{item.passage_end_char ?? '—'}
              </p>
            </article>
          ))}

          <h3>Prediction (experimental, where applicable)</h3>
          {result.outcome_prediction ? (
            <p>Predicted label: {result.outcome_prediction.predicted_label}</p>
          ) : (
            <p>Skipped{result.prediction_skipped_reason ? `: ${result.prediction_skipped_reason}` : '.'}</p>
          )}

          <h3>Conclusion</h3>
          <p>{result.conclusion?.text ?? '—'}</p>

          <h3>Uncertainty / limitations</h3>
          <p>{result.uncertainty ?? '—'}</p>

          <div className="row">
            <button type="button" onClick={onLoadAudit}>
              Load audit record
            </button>
          </div>
          {audit !== null && <pre>{JSON.stringify(audit, null, 2)}</pre>}
        </section>
      )}

      <section aria-label="experiments">
        <h2>4. Experiment metadata</h2>
        <button type="button" onClick={onLoadExperiments}>
          Load E1–E4 metadata
        </button>
        {experiments && (
          <ul>
            {experiments.map((experiment) => (
              <li key={experiment.id}>
                <strong>{experiment.id}</strong> — {experiment.name} ({experiment.status})
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
