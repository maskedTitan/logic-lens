# Logic-Lens: Business Logic Extractor

**A RAG-based CLI tool that translates legacy codebases into clear business requirements.**

![Status](https://img.shields.io/badge/Status-MVP_Complete-green)
![Stack](https://img.shields.io/badge/Stack-LangChain_|_OpenAI_|_ChromaDB-blue)

## The Problem
Stakeholders and Product Managers often face a "Knowledge Black Box" with legacy codebases. To answer basic business questions (e.g., *"Does the discount apply before or after tax?"*), they rely on expensive engineering time or stale documentation. Generic AI coding assistants focus on *syntax* (loop structure) rather than *semantics* (business rules).

## The Solution
**Logic-Lens** is a local Retrieval-Augmented Generation (RAG) tool designed to extract business logic from Python repositories.
*   **Ingests** local source code (e.g., [Django-Oscar](https://github.com/django-oscar/django-oscar)) into a vector database.
*   **Extracts** logic using a system prompt engineered for "Product/Business" translation.
*   **Cites** specific filenames as authoritative sources to ensure trust.

---

## Demo Output

**User Question:**  
`python src/query.py "How is the basket total calculated?"`

**System Response:**
```text
[Logic-Lens Analysis]

tl;dr Answer:
The basket total is the sum of line items plus applicable charges, dependent on tax availability.

Business Rules:
- Tax is ONLY calculated if all line items report known tax values.
- Discounts are applied on a line-item basis before aggregation.
- Shipping charges are added after subtotal calculation.

Technical Constraints:
- [Dependency] Relies on third-party integrations for surcharge calculations.
- [Risk] Logic assumes positive integer values for quantity.

Source Authority:
- basket/models.py
- order/utils.py
