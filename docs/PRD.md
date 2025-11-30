# 📄 Product Requirements Document: Logic-Lens (v1.0)

| Metadata | Details |
| :--- | :--- |
| **Feature** | Logic-Lens Core CLI |

## 1. Problem Statement
**The "Black Box" Effect:**
In 85% of legacy software interactions, Product Managers must interrupt Engineering to answer basic questions about business logic (e.g., *"Does the discount apply before or after tax?"*). This causes:
1.  **High Context Switching Costs** for developers.
2.  **Delayed Decision Making** for stakeholders.
3.  **Risk of Drift:** Documentation is rarely in sync with the actual code.

## 2. Business Goal & Opportunity
By automating the extraction of business logic, we aim to:
*   **Reduce "Information Requests" to Engineering by 40%.**
*   Reduce "Time-to-Answer" for simple logic questions from ~4 hours (async slack gap) to <1 minute.

## 3. Scope
### ✅ In Scope (MVP)
*   **Ingestion:** Parsing local Python repositories (`.py` files only).
*   **Storage:** Local Vector Database (ChromaDB) for persistence.
*   **Interface:** Command Line Interface (CLI) for Q&A.
*   **Intelligence:** Extraction of "Business Rules" vs "Technical Implementation."
*   **Citation:** Returning specific filenames as sources.

### ❌ Out of Scope (Phase 1)
*   Frontend UI (Web Dashboard).
*   Integration with GitHub Webhooks (Real-time updates).
*   Parsing of non-Python files (Javascript, SQL, CSS).
*   Multi-repo support (Ingesting 2+ repos at once).

## 4. User Personas
*   **Primary: The "Non-Coding" Technical PM.** Can read JSON but cannot trace a 10-file dependency chain in Python. Needs authoritative answers to write specs.
*   **Secondary: The QA Lead.** Needs to understand edge cases to write test plans (e.g., *"What happens if cart total is exactly $0?"*).

## 5. Functional Requirements (Detailed)
| ID | Requirement | Acceptance Criteria | Priority |
| :--- | :--- | :--- | :--- |
| **FR-01** | **Ingest Target Repo** | User runs `python src/ingest.py` and receives a "Success" message within 60s for a <1GB repo. | P0 |
| **FR-02** | **Context Chunking** | Code must be split into chunks >1000 chars with 200 char overlap to preserve function context. | P0 |
| **FR-03** | **Persona Prompting** | AI Output must separate "Business Rules" from "Technical details" (as verified by test set). | P0 |
| **FR-04** | **Source Attribution** | Every answer must include at least one valid file path (e.g., `basket/models.py`). | P0 |
| **FR-05** | **Ambiguity Handling** | If logic is not found, System explicitly states "Not found in context" rather than hallucinating. | P1 |

## 6. Technical Constraints
*   **Model:** Must use OpenAI `gpt-4o` for reasoning capabilities; `gpt-3.5` deemed insufficient for code analysis during Alpha testing.
*   **Environment:** Must run locally on Python 3.9+.
*   **Cost:** Ingestion cost must not exceed $0.50 per 100 files.
