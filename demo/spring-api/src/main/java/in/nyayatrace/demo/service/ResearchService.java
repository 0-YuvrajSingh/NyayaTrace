package in.nyayatrace.demo.service;

import com.fasterxml.jackson.databind.JsonNode;
import in.nyayatrace.demo.audit.AuditRecord;
import in.nyayatrace.demo.audit.AuditStore;
import in.nyayatrace.demo.client.MlClient;
import in.nyayatrace.demo.model.ResearchRequest;
import java.time.Instant;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import org.springframework.stereotype.Service;

/**
 * Orchestrates one research request: forwards the frozen E4 path to the
 * Python service, records the minimal audit trail, returns the envelope.
 * No BM25/provenance/model logic is re-implemented here.
 */
@Service
public class ResearchService {

  private final MlClient mlClient;
  private final AuditStore auditStore;

  public ResearchService(MlClient mlClient, AuditStore auditStore) {
    this.mlClient = mlClient;
    this.auditStore = auditStore;
  }

  public Map<String, Object> research(ResearchRequest request) {
    Map<String, Object> mlBody = new LinkedHashMap<>();
    mlBody.put("query", request.query());
    mlBody.put("query_id", request.effectiveQueryId());
    mlBody.put("query_year", request.effectiveQueryYear());
    mlBody.put("candidate_k", request.effectiveCandidateK());
    mlBody.put("top_k", request.effectiveTopK());
    mlBody.put("include_prediction", request.effectiveIncludePrediction());

    JsonNode result = mlClient.postQuery(mlBody);
    String requestId = UUID.randomUUID().toString();

    List<String> chunkIds = new ArrayList<>();
    JsonNode evidence = result.path("supporting_evidence");
    if (evidence.isArray()) {
      evidence.forEach(item -> {
        if (item.hasNonNull("chunk_id")) {
          chunkIds.add(item.get("chunk_id").asText());
        }
      });
    }
    JsonNode verification = result.path("citation_verification");
    auditStore.put(new AuditRecord(
        requestId,
        Instant.now(),
        result.path("experiment").asText("E4"),
        result.path("meta").path("index_version").asText(null),
        result.path("selection_version").asText(null),
        result.path("query_id").asText(request.effectiveQueryId()),
        result.path("query_year").asInt(request.effectiveQueryYear()),
        List.copyOf(chunkIds),
        verification.path("status").asText(null),
        verification.path("passed_count").asInt(0),
        toPlain(result.path("status_counts")),
        "ok"));

    Map<String, Object> envelope = new LinkedHashMap<>();
    envelope.put("request_id", requestId);
    envelope.put("result", result);
    return envelope;
  }

  private static Object toPlain(JsonNode node) {
    if (node.isObject() || node.isArray()) {
      return node.toString();
    }
    if (node.isNumber()) {
      return node.numberValue();
    }
    if (node.isBoolean()) {
      return node.booleanValue();
    }
    return node.isNull() ? null : node.asText();
  }
}
