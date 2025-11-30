# 📊 Success Metrics & Analytics Strategy

## 1. North Star Metric
**"Engineering Hours Saved"**
*   *Definition:* (Number of Queries) * (Avg Time for Dev to Answer - Avg Time for Logic-Lens to Answer).
*   *Assumption:* Avg Dev interruption takes 20 mins. Logic-Lens takes 1 min.

## 2. Key Performance Indicators (KPIs)

| Metric Category | Metric Name | Target (MVP) | How to Measure |
| :--- | :--- | :--- | :--- |
| **Adoption** | Weekly Active Users (WAU) | 5 PMs | CLI Usage Logs |
| **Quality** | "Thumbs Up" Ratio | > 80% | Prompt user "Was this helpful? (y/n)" after query |
| **Performance** | Ingestion Success Rate | 100% | Error logs during `ingest.py` |
| **Reliability** | Hallucination Rate | < 5% | Manual audit of 20 random queries/week |

## 3. Instrumentation Plan (Logging)
To measure these metrics, we will implement a lightweight logger in `src/utils.py` that writes to a local `usage.json` file.

**Log Event Schema:**
```json
{
  "timestamp": "2025-11-30T10:00:00Z",
  "event_type": "query",
  "query_length": 45,
  "response_time_ms": 3500,
  "sources_found": 3,
  "user_feedback": "positive"
}