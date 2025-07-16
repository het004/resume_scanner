from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List


def preprocess_documents(
    docs: List[Document], 
    chunk_size: int = 500, 
    chunk_overlap: int = 50
) -> List[Document]:
    """
    Preprocesses and splits documents into smaller chunks.

    Args:
        docs (List[Document]): Raw documents loaded using LangChain.
        chunk_size (int): Max size of each text chunk (default: 500).
        chunk_overlap (int): Overlap between chunks for better context (default: 50).

    Returns:
        List[Document]: List of chunked Document objects with metadata preserved.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunked_docs = text_splitter.split_documents(docs)
    return chunked_docs
