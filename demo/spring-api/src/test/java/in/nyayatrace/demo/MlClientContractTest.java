package in.nyayatrace.demo;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.header;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.jsonPath;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.method;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.requestTo;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withSuccess;

import com.fasterxml.jackson.databind.JsonNode;
import in.nyayatrace.demo.audit.AuditStore;
import in.nyayatrace.demo.client.MlClient;
import in.nyayatrace.demo.config.AppConfig.MlEndpoint;
import in.nyayatrace.demo.model.ResearchRequest;
import in.nyayatrace.demo.service.ResearchService;
import java.util.Map;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.client.RestClientTest;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.test.web.client.MockRestServiceServer;
import org.springframework.web.client.RestTemplate;

/**
 * Integration-seam contract test: verifies the exact Spring→FastAPI HTTP
 * exchange (URL, internal token, request fields) and the audit linkage for
 * the frozen week-10 replay query shape.
 */
@RestClientTest
class MlClientContractTest {

  @Autowired
  RestTemplateBuilder builder;

  private MockRestServiceServer server;
  private ResearchService service;
  private AuditStore auditStore;

  @BeforeEach
  void setUp() {
    RestTemplate restTemplate = builder.build();
    server = MockRestServiceServer.bindTo(restTemplate).build();
    auditStore = new AuditStore();
    MlClient client = new MlClient(restTemplate, new MlEndpoint("http://ml:8001", "internal-test"));
    service = new ResearchService(client, auditStore);
  }

  @Test
  void week10QueryForwardsContractAndLinksAudit() {
    String mlBody = """
        {"experiment":"E4","run_id":"00000000-0000-4000-8000-000000000001",
         "query_id":"week10-replay-01","query_year":2020,
         "supporting_evidence":[{"evidence_id":"E1","chunk_id":"S_2000_1_1_1::p0001::c001"}],
         "citation_verification":{"status":"passed","passed_count":1,"checks":[]},
         "status_counts":{"eligible":100},"selection_version":"week11-bm25-salient-terms-preranked-temporal-v3",
         "meta":{"index_version":"fts5-bm25-unicode61-temporal-v2"}}""";
    server.expect(requestTo("http://ml:8001/research/query"))
        .andExpect(method(HttpMethod.POST))
        .andExpect(header("X-Internal-Token", "internal-test"))
        .andExpect(jsonPath("$.query").value("anticipatory bail section 438"))
        .andExpect(jsonPath("$.query_id").value("week10-replay-01"))
        .andExpect(jsonPath("$.query_year").value(2020))
        .andRespond(withSuccess(mlBody, MediaType.APPLICATION_JSON));

    Map<String, Object> envelope = service.research(
        new ResearchRequest("anticipatory bail section 438", "week10-replay-01", 2020, 100, 5, false));

    assertEquals("week10-replay-01",
        ((JsonNode) envelope.get("result")).get("query_id").asText());
    String requestId = (String) envelope.get("request_id");
    assertEquals("passed", auditStore.get(requestId).citationStatus());
    assertEquals("S_2000_1_1_1::p0001::c001", auditStore.get(requestId).evidenceChunkIds().get(0));
    server.verify();
  }
}
