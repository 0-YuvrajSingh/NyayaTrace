package in.nyayatrace.demo.config;

import java.time.Duration;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
public class AppConfig {

  @Bean
  public RestTemplate restTemplate(RestTemplateBuilder builder) {
    return builder.setConnectTimeout(Duration.ofSeconds(10)).setReadTimeout(Duration.ofSeconds(300)).build();
  }

  @Bean
  public MlEndpoint mlEndpoint(@Value("${ml.base-url:http://127.0.0.1:8001}") String baseUrl,
      @Value("${ml.internal-token:}") String internalToken) {
    return new MlEndpoint(baseUrl, internalToken);
  }

  /** ML service address plus the internal caller token (env-supplied, never committed). */
  public record MlEndpoint(String baseUrl, String internalToken) {}
}
