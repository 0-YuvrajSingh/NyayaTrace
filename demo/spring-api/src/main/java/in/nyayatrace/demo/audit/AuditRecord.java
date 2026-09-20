package in.nyayatrace.demo.audit;

import java.time.Instant;
import java.util.List;

/**
 * Minimal audit record for one research request. Stores orchestration
 * metadata only (no personal data, no secrets): identifiers, versions,
 * evidence linkage, verification/temporal outcomes, and result status.
 */
public record AuditRecord(
    String requestId,
    Instant timestamp,
    String experimentId,
    String indexVersion,
    String selectionVersion,
    String queryId,
    int queryYear,
    List<String> evidenceChunkIds,
    String citationStatus,
    int citationPassedCount,
    Object temporalStatusCounts,
    String resultStatus) {}
