from typing import Dict, Any
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.components.loader import load_document
from src.components.Text_preprcessing import preprocess_documents
from src.components.push_database import push_raw_documents
from src.components.embedding_faiss import embed_and_store_faiss_ollama
from src.components.langchain_retrival import similarity_search
from src.components.scoring_reportformating import generate_full_report


from src.loggers import logger


def run_resume_pipeline(
    resume_path: str,
    jd_path: str,
    resume_index_name: str = "resume_index",
    model_name: str = "nomic-embed-text"
) -> Dict[str, str]:


    # STEP 1: Load resume and JD
    logger.logging.info("📂 Loading documents...")
    resume_docs = load_document(resume_path)
    jd_docs = load_document(jd_path)

    # STEP 2: Push raw to MongoDB
    logger.logging.info("🗃️ Pushing raw resume and JD to MongoDB...")
    push_raw_documents(resume_docs, doc_type="resume", file_name=resume_path)
    push_raw_documents(jd_docs, doc_type="job_description", file_name=jd_path)

    # STEP 3: Preprocess (chunk) documents
    logger.logging.info("🧹 Preprocessing documents...")
    resume_chunks = preprocess_documents(resume_docs)
    jd_chunks = preprocess_documents(jd_docs)

    # STEP 4: Embed resume chunks and store to FAISS
    logger.logging.info("📌 Embedding resume chunks with FAISS...")
    embed_and_store_faiss_ollama(resume_chunks, index_name=resume_index_name, model_name=model_name)

    # STEP 5: Prepare query from JD and run similarity search
    logger.logging.info("🔎 Performing similarity search against JD...")
    jd_text = " ".join([doc.page_content for doc in jd_chunks])
    top_resume_chunks = similarity_search(
        query=jd_text,
        index_name=resume_index_name,
        k=5,
        model_name=model_name
    )

    # STEP 6: Generate report
    logger.logging.info("🧠 Generating final report (SWOT, ATS, Suggestions)...")
    report = generate_full_report(resume_chunks=top_resume_chunks, jd_text=jd_text)

    logger.logging.info("✅ Pipeline completed successfully.")
    return report