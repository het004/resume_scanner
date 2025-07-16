import os
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document


# Directory where FAISS indexes are stored
FAISS_DIR = "vector_store"
os.makedirs(FAISS_DIR, exist_ok=True)


def embed_and_store_faiss_ollama(
    documents: List[Document],
    index_name: str,
    model_name: str = "nomic-embed-text"
) -> FAISS:
    """
    Embeds and stores documents using Ollama + FAISS.

    Args:
        documents (List[Document]): Preprocessed chunks of text.
        index_name (str): Unique name for the FAISS index.
        model_name (str): Ollama model to use.

    Returns:
        FAISS vector store object.
    """
    embeddings = OllamaEmbeddings(model=model_name)
    vectorstore = FAISS.from_documents(documents, embedding=embeddings)

    index_path = os.path.join(FAISS_DIR, f"{index_name}_faiss")
    vectorstore.save_local(index_path)

    print(f"✅ FAISS index saved to: {index_path}")
    return vectorstore


def load_faiss_index_ollama(
    index_name: str,
    model_name: str = "nomic-embed-text"
) -> FAISS:
    """
    Loads an existing FAISS vector store using Ollama embeddings.

    Args:
        index_name (str): Name used when saving the index.
        model_name (str): Ollama embedding model to match.

    Returns:
        FAISS vector store.
    """
    index_path = os.path.join(FAISS_DIR, f"{index_name}_faiss")
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"FAISS index not found at {index_path}")

    embeddings = OllamaEmbeddings(model=model_name)
    return FAISS.load_local(
        folder_path=index_path,
        embeddings=embeddings,
        allow_dangerous_deserialization=True  # ✅ Enable if you trust the file
    )
