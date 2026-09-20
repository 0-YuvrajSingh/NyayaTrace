package in.nyayatrace.demo.controller;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import in.nyayatrace.demo.audit.AuditRecord;
import in.nyayatrace.demo.audit.AuditStore;
import in.nyayatrace.demo.client.MlClient;
import in.nyayatrace.demo.client.MlClient.MlServiceException;
import in.nyayatrace.demo.model.ResearchRequest;
import in.nyayatrace.demo.service.ResearchService;
import jakarta.validation.Valid;
import java.io.IOException;
import java.io.InputStream;
import java.util.Map;
import org.springframework.core.io.ClassPathResource;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class ResearchController {

  private final ResearchService researchService;
  private final MlClient mlClient;
  private final AuditStore auditStore;
  private final ObjectMapper objectMapper;

  public ResearchController(ResearchService researchService, MlClient mlClient,
      AuditStore auditStore, ObjectMapper objectMapper) {
    this.researchService = researchService;
    this.mlClient = mlClient;
    this.auditStore = auditStore;
    this.objectMapper = objectMapper;
  }

  @GetMapping("/health")
  public Map<String, Object> health() {
    JsonNode ml;
    String mlStatus = "ok";
    try {
      ml = mlClient.getHealth();
    } catch (MlServiceException error) {
      mlStatus = "unreachable";
      ml = objectMapper.createObjectNode();
    }
    return Map.of("status", "ok", "service", "spring-api", "ml_status", mlStatus, "ml", ml);
  }

  @PostMapping("/research/query")
  public Map<String, Object> query(@Valid @RequestBody ResearchRequest request) {
    if (request.effectiveTopK() > request.effectiveCandidateK()) {
      throw new BadRequestException("candidate_k must be at least top_k");
    }
    return researchService.research(request);
  }

  @GetMapping("/experiments")
  public JsonNode experiments() throws IOException {
    try (InputStream stream = new ClassPathResource("experiments.json").getInputStream()) {
      return objectMapper.readTree(stream);
    }
  }

  @GetMapping("/audit/{requestId}")
  public ResponseEntity<AuditRecord> audit(@PathVariable String requestId) {
    AuditRecord record = auditStore.get(requestId);
    if (record == null) {
      return ResponseEntity.notFound().build();
    }
    return ResponseEntity.ok(record);
  }

  @ExceptionHandler(MlServiceException.class)
  public ResponseEntity<Map<String, String>> mlUnavailable(MlServiceException error) {
    return ResponseEntity.status(error.getStatusCode()).body(Map.of("error", error.getMessage()));
  }

  @ExceptionHandler(BadRequestException.class)
  public ResponseEntity<Map<String, String>> badRequest(BadRequestException error) {
    return ResponseEntity.badRequest().body(Map.of("error", error.getMessage()));
  }

  static class BadRequestException extends RuntimeException {
    BadRequestException(String message) {
      super(message);
    }
  }
}
