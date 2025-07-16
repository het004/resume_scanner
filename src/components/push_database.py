import os
from pymongo import MongoClient
from dotenv import load_dotenv
from langchain_core.documents import Document
from typing import List

# Load env vars
load_dotenv()

# Get config
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "resume_scanner")
COLLECTION_NAME = os.getenv("RAW_COLLECTION", "raw_uploads")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


def push_raw_documents(docs: List[Document], doc_type: str, file_name: str):
    """
    Push raw resume or JD content to MongoDB.

    Args:
        docs (List[Document]): List of raw LangChain Documents.
        doc_type (str): Either "resume" or "job_description".
        file_name (str): Original file name for metadata.
    """
    for doc in docs:
        record = {
            "type": doc_type,
            "file_name": file_name,
            "content": doc.page_content,
            "source": doc.metadata.get("source", ""),
        }
        collection.insert_one(record)
