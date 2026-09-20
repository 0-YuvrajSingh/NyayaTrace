package in.nyayatrace.demo.client;

import com.fasterxml.jackson.databind.JsonNode;
import in.nyayatrace.demo.config.AppConfig.MlEndpoint;
import java.util.Map;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestTemplate;

/** Thin HTTP client for the Python ML service. No research logic lives here. */
@Component
public class MlClient {

  private final RestTemplate restTemplate;
  private final MlEndpoint endpoint;

  public MlClient(RestTemplate restTemplate, MlEndpoint endpoint) {
    this.restTemplate = restTemplate;
    this.endpoint = endpoint;
  }

  public JsonNode postQuery(Map<String, Object> body) {
    HttpHeaders headers = new HttpHeaders();
    headers.setContentType(MediaType.APPLICATION_JSON);
    if (!endpoint.internalToken().isEmpty()) {
      headers.set("X-Internal-Token", endpoint.internalToken());
    }
    try {
      ResponseEntity<JsonNode> response = restTemplate.exchange(
          endpoint.baseUrl() + "/research/query", HttpMethod.POST,
          new HttpEntity<>(body, headers), JsonNode.class);
      return response.getBody();
    } catch (ResourceAccessException error) {
      throw new MlServiceException(503, "research service is unreachable");
    }
  }

  public JsonNode getHealth() {
    try {
      return restTemplate.getForObject(endpoint.baseUrl() + "/health", JsonNode.class);
    } catch (ResourceAccessException error) {
      throw new MlServiceException(503, "research service is unreachable");
    }
  }

  /** Carries an ML-service failure across the orchestration boundary. */
  public static class MlServiceException extends RuntimeException {
    private final int statusCode;

    public MlServiceException(int statusCode, String message) {
      super(message);
      this.statusCode = statusCode;
    }

    public int getStatusCode() {
      return statusCode;
    }
  }
}
