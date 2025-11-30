import argparse
import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# CONFIGURATION
DB_DIR = "./chroma_db"

# THE PRODUCT "SECRET SAUCE" (System Prompt)
PROMPT_TEMPLATE = """
You are Logic-Lens, a Senior Technical Product Manager. 
Your goal is to explain the BUSINESS LOGIC of the provided code to a non-technical stakeholder.

CONTEXT FROM CODEBASE:
{context}

USER QUESTION: 
{question}

INSTRUCTIONS:
1. **Analyze** the provided code chunks.
2. **Translate** the logic into clear Business Rules.
3. **Format** your answer exactly like this:

---
### 🤖 Logic-Lens Analysis

**tl;dr Answer:** 
(One sentence summary)

**👔 Business Rules:**
* (Rule 1)
* (Rule 2)

**⚠️ Risk & Technical Constraints:**
* [Hardcoded Values]: (Did you find any specific numbers? e.g., Tax=0.20)
* [Dependencies]: (Does this touch Payments, Email, or Auth?)

**📂 Source Authority:**
(List the filenames where you found this logic, e.g., `basket/models.py`)
---

If the code is ambiguous, say "The provided context does not cover this specific logic." Do not hallucinate.
"""

def query_logic(question):
    # 1. Load the Memory
    # FIX: We changed 'embedding' to 'embedding_function' here
    db = Chroma(persist_directory=DB_DIR, embedding_function=OpenAIEmbeddings())

    # 2. Retrieval (The "Search")
    results = db.similarity_search(question, k=5)
    
    # Context Construction
    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    
    # 3. Generation (The "Reasoning")
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    
    # Using GPT-4o for best logic reasoning
    model = ChatOpenAI(model="gpt-4o") 
    
    chain = prompt | model
    
    print(f"\n🤔 Analyzing {len(results)} code chunks for: '{question}'...\n")
    
    response = chain.invoke({"context": context_text, "question": question})

    print(response.content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("question", type=str, help="The business question to ask the codebase")
    args = parser.parse_args()
    query_logic(args.question)