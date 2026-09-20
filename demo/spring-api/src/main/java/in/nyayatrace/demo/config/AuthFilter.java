package in.nyayatrace.demo.config;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

/**
 * Minimal local-demo bearer authentication. The expected token comes only
 * from the {@code DEMO_API_TOKEN} environment variable; nothing is
 * hardcoded. {@code GET /api/health} stays open so orchestration probes work.
 */
@Component
public class AuthFilter extends OncePerRequestFilter {

  private final String expectedToken;

  public AuthFilter(@Value("${demo.api-token:}") String expectedToken) {
    this.expectedToken = expectedToken == null ? "" : expectedToken;
  }

  @Override
  protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response,
      FilterChain chain) throws ServletException, IOException {
    String path = request.getRequestURI();
    if (path.equals("/api/health") || !path.startsWith("/api/")) {
      chain.doFilter(request, response);
      return;
    }
    String presented = request.getHeader("Authorization");
    if (presented != null && presented.startsWith("Bearer ")) {
      presented = presented.substring(7);
    } else {
      presented = null;
    }
    boolean ok = !expectedToken.isEmpty() && presented != null
        && MessageDigest.isEqual(presented.getBytes(StandardCharsets.UTF_8),
            expectedToken.getBytes(StandardCharsets.UTF_8));
    if (!ok) {
      response.setStatus(HttpStatus.UNAUTHORIZED.value());
      response.setContentType(MediaType.APPLICATION_JSON_VALUE);
      response.getWriter().write("{\"error\":\"unauthorized\"}");
      return;
    }
    chain.doFilter(request, response);
  }
}
