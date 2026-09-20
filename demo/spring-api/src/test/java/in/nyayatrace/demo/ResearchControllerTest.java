package in.nyayatrace.demo;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyMap;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import in.nyayatrace.demo.client.MlClient;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@TestPropertySource(properties = "demo.api-token=test-token")
class ResearchControllerTest {

  private static final String TOKEN = "Bearer test-token";

  @Autowired
  MockMvc mvc;

  @Autowired
  ObjectMapper objectMapper;

  @MockBean
  MlClient mlClient;

  private ObjectNode mlEnvelope() {
    ObjectNode result = objectMapper.createObjectNode();
    result.put("experiment", "E4");
    result.put("run_id", "00000000-0000-4000-8000-000000000001");
    result.put("query_id", "week10-replay-01");
    result.put("query_year", 2020);
    ObjectNode verification = result.putObject("citation_verification");
    verification.put("status", "passed");
    verification.put("passed_count", 1);
    result.putArray("supporting_evidence").addObject().put("chunk_id", "S_2000_1_1_1::p0001::c001");
    result.putObject("status_counts").put("eligible", 100);
    return result;
  }

  @Test
  void healthIsOpenWithoutAuth() throws Exception {
    when(mlClient.getHealth()).thenReturn(objectMapper.createObjectNode().put("status", "ok"));
    mvc.perform(get("/api/health"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.status").value("ok"));
  }

  @Test
  void queryWithoutTokenIsRejected() throws Exception {
    mvc.perform(post("/api/research/query").contentType(MediaType.APPLICATION_JSON)
        .content("{\"query\":\"anticipatory bail section 438\"}"))
        .andExpect(status().isUnauthorized());
  }

  @Test
  void queryWithBadTokenIsRejected() throws Exception {
    mvc.perform(post("/api/research/query").header("Authorization", "Bearer wrong")
        .contentType(MediaType.APPLICATION_JSON)
        .content("{\"query\":\"anticipatory bail section 438\"}"))
        .andExpect(status().isUnauthorized());
  }

  @Test
  void authenticatedQueryReturnsEnvelopeAndAudit() throws Exception {
    when(mlClient.postQuery(anyMap())).thenReturn(mlEnvelope());
    String body = mvc.perform(post("/api/research/query").header("Authorization", TOKEN)
        .contentType(MediaType.APPLICATION_JSON)
        .content("{\"query\":\"anticipatory bail section 438\",\"query_id\":\"week10-replay-01\",\"query_year\":2020}"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.request_id").exists())
        .andExpect(jsonPath("$.result.experiment").value("E4"))
        .andReturn().getResponse().getContentAsString();
    String requestId = objectMapper.readTree(body).get("request_id").asText();
    mvc.perform(get("/api/audit/" + requestId).header("Authorization", TOKEN))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.requestId").value(requestId))
        .andExpect(jsonPath("$.evidenceChunkIds[0]").value("S_2000_1_1_1::p0001::c001"))
        .andExpect(jsonPath("$.citationStatus").value("passed"));
  }

  @Test
  void experimentsEndpointListsE1ToE4() throws Exception {
    mvc.perform(get("/api/experiments").header("Authorization", TOKEN))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.experiments[0].id").value("E1"))
        .andExpect(jsonPath("$.experiments[1].id").value("E2"))
        .andExpect(jsonPath("$.experiments[2].id").value("E3"))
        .andExpect(jsonPath("$.experiments[3].id").value("E4"));
  }

  @Test
  void unknownAuditIdIs404() throws Exception {
    mvc.perform(get("/api/audit/does-not-exist").header("Authorization", TOKEN))
        .andExpect(status().isNotFound());
  }

  @Test
  void invalidRequestIs400() throws Exception {
    when(mlClient.postQuery(any())).thenReturn(mlEnvelope());
    mvc.perform(post("/api/research/query").header("Authorization", TOKEN)
        .contentType(MediaType.APPLICATION_JSON)
        .content("{\"query\":\"\"}"))
        .andExpect(status().isBadRequest());
    mvc.perform(post("/api/research/query").header("Authorization", TOKEN)
        .contentType(MediaType.APPLICATION_JSON)
        .content("{\"query\":\"x\",\"top_k\":5,\"candidate_k\":2}"))
        .andExpect(status().isBadRequest());
  }
}
