# 🎟 User Stories (Jira Export)

## Epic: Core Query Engine

### Story 1: Ingest Logic from Local Directory
**As a** Product Manager,  
**I want to** point Logic-Lens at a local folder containing the `django-oscar` repo,  
**So that** I can index the codebase without needing cloud access or API integrations.

**Acceptance Criteria (Gherkin):**
*   **GIVEN** a valid directory path `./data/target_repo` containing `.py` files
*   **WHEN** I run the `ingest.py` script
*   **THEN** the system should create a `chroma_db` folder
*   **AND** the system should log the number of files processed
*   **AND** non-python files (images, css) should be ignored to save costs.

**Story Points:** 3  
**Priority:** High

---

### Story 2: Source Citation in Answers
**As a** Compliance Officer,  
**I want to** see exactly which file the answer came from,  
**So that** I can verify the logic myself if necessary and trust the AI's output.

**Acceptance Criteria:**
*   **GIVEN** a query about "Tax Calculation"
*   **WHEN** the AI generates a response
*   **THEN** the response must contain a section `📂 Source Authority`
*   **AND** it must list the filename (e.g., `partner/strategy.py`)
*   **AND** if multiple files contributed to the answer, list top 3.

**Story Points:** 2  
**Priority:** Medium

---

### Story 3: "High Risk" Flagging
**As a** Tech Lead,  
**I want** the system to explicitly warn me if a feature touches sensitive systems,  
**So that** I don't accidentally propose changes to critical infrastructure without review.

**Acceptance Criteria:**
*   **GIVEN** the code contains keywords: `Auth`, `Payment`, `Stripe`, `Password`
*   **WHEN** the system answers a question about that code
*   **THEN** it should append a `⚠️ [HIGH RISK]` tag to the Technical Constraints section.

**Story Points:** 5  
**Priority:** Medium