# 🏗 The Architecture: How Logic-Lens Works

| Document Type | Technical Explainer |
| :--- | :--- |
| **Audience** | Non-Technical Stakeholders & Product Teams |
| **Goal** | Demystify the "Magic" behind the AI |

## 1. The High-Level Concept: RAG (Retrieval-Augmented Generation)

Most people think AI "knows" everything. It doesn't.
*   **ChatGPT** knows general facts (history, coding syntax, recipes) because it was trained on the public internet.
*   **ChatGPT** does *not* know your private business logic because it has never seen your codebase.

We cannot "train" a new model on your code (it costs millions and takes months). Instead, we use a technique called **RAG**.

### The Analogy: The Open-Book Exam
*   **Traditional AI:** Asking a student to take a test from memory. (They will fail if they haven't studied the specific topic).
*   **RAG (Logic-Lens):** Giving the student a textbook (your code) and letting them look up the answer before writing the essay.

---

## 2. The Tech Stack (The "Legos")

To build this "Open-Book" system, we combine four specific technologies. Here is how they fit together:

### A. LangChain (The General Contractor)
*   **What it is:** The framework that connects all the different tools (Database, AI, Data Loaders).
*   **Role in Logic-Lens:** It acts as the pipeline. It handles the "hand-offs"—taking the code files, passing them to the database, retrieving them, and sending them to OpenAI. Without LangChain, we'd have to write complex API glue code manually.

### B. Embeddings (The Translator)
*   **What it is:** Computers don't understand English; they understand Math. "Embeddings" turn text into a long list of numbers (vectors).
*   **The Magic:** Concepts that are *similar* end up with similar numbers.
    *   *"Basket"* and *"Cart"* will be mathematically close.
    *   *"Basket"* and *"User Authentication"* will be mathematically far apart.
*   **Role in Logic-Lens:** We use `OpenAIEmbeddings` to translate your Python code into vectors so we can search it by "meaning," not just by keyword.

### C. ChromaDB (The Memory)
*   **What it is:** A Vector Database. Unlike a standard SQL database (Excel-style rows and columns), a Vector DB stores data spatially based on meaning.
*   **Role in Logic-Lens:** This is where the "Textbook" lives. When we ingest the codebase, we chop it up and store it here. It allows us to query the database with a question like *"How do refunds work?"* and get back the 5 specific snippets of code that discuss refunds.

### D. GPT-4o (The Brain)
*   **What it is:** The Large Language Model (LLM).
*   **Role in Logic-Lens:** It does the reading and writing.
    1.  It reads the snippets we retrieved from ChromaDB.
    2.  It reads your specific User Question.
    3.  It follows our **System Prompt** ("Act as a PM...") to synthesize the answer.

---

## 3. The Step-by-Step Workflow

Here is exactly what happens when you run the application:

### Phase 1: Ingestion (The "Study" Phase)
*Runs via `src/ingest.py`*

1.  **Load:** We scan the `django-oscar` folder for `.py` files.
2.  **Split:** We cannot feed a 10,000-line file to the AI (it loses focus). We use a `RecursiveCharacterTextSplitter` to chop the code into "Chunks" of 1,500 characters.
    *   *PM Note:* We keep a 300-character overlap between chunks so we don't accidentally cut a sentence in half.
3.  **Embed & Store:** We send these chunks to OpenAI to turn them into numbers, then save them into `chroma_db` (our local folder).

### Phase 2: Query (The "Exam" Phase)
*Runs via `src/query.py`*

1.  **User Question:** You ask: *"How is tax calculated?"*
2.  **Vector Search:** The system converts your question into numbers and looks in `chroma_db` for the 5 chunks of code that are mathematically closest to "Tax Calculation."
3.  **Context Construction:** The system takes those 5 code chunks and pastes them into a prompt.
    > *Prompt:* "Here is some code I found: [Paste Code Snippets]. Based on this, answer the question: [User Question]."
4.  **Generation:** GPT-4o reads the prompt, analyzes the logic, and writes the plain-english summary.

---

## 4. Why this Architecture? (Trade-off Analysis)

As Product Managers, we make decisions based on Cost, Quality, and Speed.

| Decision | Alternative | Why we chose this path |
| :--- | :--- | :--- |
| **RAG** | Fine-Tuning a Model | **RAG is cheaper and faster.** Fine-tuning requires months of training data and maintenance. RAG works instantly on new data. |
| **ChromaDB** | Pinecone / Weaviate | **Chroma is local and free.** For an internal tool, we don't need the complexity of a cloud vector database. |
| **OpenAI GPT-4o** | Llama 3 (Local) | **Logic requires reasoning.** Local models are good for privacy, but GPT-4o is currently the state-of-the-art for complex logic extraction. 