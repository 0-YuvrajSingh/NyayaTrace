package in.nyayatrace.demo.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/** Research request DTO. Mirrors the FastAPI {@code ResearchQuery} schema. */
public record ResearchRequest(
    @NotBlank @Size(max = 20000) String query,
    @JsonProperty("query_id") @Size(max = 128) String queryId,
    @JsonProperty("query_year") @Min(1900) @Max(2100) Integer queryYear,
    @JsonProperty("candidate_k") @Min(1) @Max(500) Integer candidateK,
    @JsonProperty("top_k") @Min(1) @Max(10) Integer topK,
    @JsonProperty("include_prediction") Boolean includePrediction) {

  public String effectiveQueryId() {
    return queryId == null || queryId.isBlank() ? "demo-query" : queryId;
  }

  public int effectiveQueryYear() {
    return queryYear == null ? 2020 : queryYear;
  }

  public int effectiveCandidateK() {
    return candidateK == null ? 100 : candidateK;
  }

  public int effectiveTopK() {
    return topK == null ? 5 : topK;
  }

  public boolean effectiveIncludePrediction() {
    return Boolean.TRUE.equals(includePrediction);
  }
}
