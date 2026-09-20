package in.nyayatrace.demo.audit;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.springframework.stereotype.Component;

/** Bounded in-memory audit store (local demo only; evicts oldest past 500). */
@Component
public class AuditStore {

  private static final int MAX_RECORDS = 500;

  private final Map<String, AuditRecord> records = Collections.synchronizedMap(
      new LinkedHashMap<>() {
        @Override
        protected boolean removeEldestEntry(Map.Entry<String, AuditRecord> eldest) {
          return size() > MAX_RECORDS;
        }
      });

  public void put(AuditRecord record) {
    records.put(record.requestId(), record);
  }

  public AuditRecord get(String requestId) {
    return records.get(requestId);
  }

  public List<String> ids() {
    synchronized (records) {
      return new ArrayList<>(records.keySet());
    }
  }
}
