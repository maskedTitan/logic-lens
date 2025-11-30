# 🛡 Risk Assessment (RAID Log)

| ID | Risk Description | Probability | Impact | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **R-01** | **Hallucination:** AI invents a business rule that doesn't exist in the code. | Medium | High | **Grounding:** Set LLM temperature to 0. System Prompt explicitly instructs "If context is missing, state 'Unknown'." |
| **R-02** | **Stale Data:** The repo updates, but the Vector DB is old. | High | Medium | **Process:** Add a generic "Last Indexed: [Date]" timestamp to every answer. Force re-indexing on startup in future versions. |
| **R-03** | **Cost Overrun:** Indexing a massive repo (>10k files) spikes OpenAI API bill. | Low | Low | **Gatekeeping:** Ingestion script has a hard limit (stop after 1000 files) and whitelist `.py` files only. |
| **R-04** | **Security Leak:** User ingests a repo containing hardcoded API keys/secrets, and sends them to OpenAI. | Low | High | **Pre-processing:** Add a Regex filter in `ingest.py` to scrub strings that look like `sk-live-...` before embedding. |
| **R-05** | **Context Window Overflow:** Logic is split across 5 files, and retrieval only finds 3. | Medium | Medium | **Architecture:** Increased chunk overlap to 300 chars. Future: Implement "Parent Document Retrieval" or Graph RAG. |
