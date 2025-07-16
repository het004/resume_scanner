import os
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document

# FAISS save path
FAISS_DIR = "vector_store"
os.makedirs(FAISS_DIR, exist_ok=True)


def embed_and_store_faiss_ollama(
    documents: List[Document], 
    index_name: str,
    model_name: str = "nomic-embed-text"
) -> FAISS:
    """
    Embed documents using Ollama's local embedding model and store in FAISS.

    Args:
        documents (List[Document]): Preprocessed LangChain Document objects.
        index_name (str): Name of FAISS index directory.
        model_name (str): Ollama model to use (default: nomic-embed-text).

    Returns:
        FAISS: FAISS vector store object.
    """
    embeddings = OllamaEmbeddings(model=model_name)
    vectorstore = FAISS.from_documents(documents, embedding=embeddings)

    index_path = os.path.join(FAISS_DIR, f"{index_name}_faiss")
    vectorstore.save_local(index_path)
    print(f"FAISS index saved at: {index_path}")
    return vectorstore


def load_faiss_index_ollama(index_name: str, model_name: str = "nomic-embed-text") -> FAISS:
    """
    Load FAISS index stored with Ollama embeddings.

    Args:
        index_name (str): Directory name of the FAISS index.
        model_name (str): Ollama model used for embeddings.

    Returns:
        FAISS: Loaded FAISS vector store.
    """
    index_path = os.path.join(FAISS_DIR, f"{index_name}_faiss")
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"FAISS index not found at: {index_path}")

    embeddings = OllamaEmbeddings(model=model_name)
    return FAISS.load_local(index_path, embeddings)
