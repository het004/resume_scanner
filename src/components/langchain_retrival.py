import os
from typing import List, Tuple
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document


def load_vectorstore(index_name: str, model_name: str = "nomic-embed-text") -> FAISS:
    """
    Loads a FAISS vector store using Ollama embeddings.

    Args:
        index_name (str): Name of the FAISS index (without _faiss).
        model_name (str): Ollama embedding model to use.

    Returns:
        FAISS: Loaded vector store.
    """
    index_path = os.path.join("vector_store", f"{index_name}_faiss")
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"Index not found at: {index_path}")

    embeddings = OllamaEmbeddings(model=model_name)

    # ✅ Safe override: enable if index is trusted (your own)
    vectorstore = FAISS.load_local(
        folder_path=index_path,
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore


def similarity_search(
    query: str,
    index_name: str,
    k: int = 5,
    model_name: str = "nomic-embed-text"
) -> List[Document]:
    """
    Retrieves top-k similar chunks using semantic search.
    """
    vectorstore = load_vectorstore(index_name, model_name)
    return vectorstore.similarity_search(query=query, k=k)


def similarity_search_with_scores(
    query: str,
    index_name: str,
    k: int = 5,
    model_name: str = "nomic-embed-text"
) -> List[Tuple[Document, float]]:
    """
    Retrieves top-k similar chunks along with similarity scores.
    """
    vectorstore = load_vectorstore(index_name, model_name)
    return vectorstore.similarity_search_with_score(query=query, k=k)
