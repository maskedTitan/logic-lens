import os
import shutil
from langchain_community.document_loaders import DirectoryLoader, PythonLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# CONFIGURATION
TARGET_DIR = "./data/target_repo"
DB_DIR = "./chroma_db"

def ingest_codebase():
    # 1. CLEANUP (Data Hygiene)
    if os.path.exists(DB_DIR):
        print(f"🧹 Cleaning up old database at {DB_DIR}...")
        shutil.rmtree(DB_DIR)

    # 2. EXTRACTION (Scope Enforcement)
    print(f"🔍 Scanning Enterprise Codebase at {TARGET_DIR}...")
    # PM Decision: Only load .py files. 
    loader = DirectoryLoader(TARGET_DIR, glob="**/*.py", loader_cls=PythonLoader)
    documents = loader.load()
    
    if not documents:
        print("❌ Error: No Python files found. Check your target directory.")
        return
        
    print(f"📄 Found {len(documents)} Python files containing Business Logic.")

    # 3. TRANSFORMATION (Chunking Strategy)
    # We use larger overlap to ensure complex logic (like nested classes) isn't cut off.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, 
        chunk_overlap=300,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"🧩 Split code into {len(chunks)} searchable chunks.")

    # 4. LOADING (The Cost Center)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ CRITICAL ERROR: OPENAI_API_KEY is missing. Create a .env file.")
        return

    print("💾 Generating Embeddings (This sends data to OpenAI)...")
    Chroma.from_documents(
        documents=chunks, 
        embedding=OpenAIEmbeddings(),
        persist_directory=DB_DIR
    )
    print("✅ Success! The 'Django-Oscar' logic is now indexed.")

if __name__ == "__main__":
    ingest_codebase()