import os
import shutil
from langchain_community.document_loaders import UnstructuredFileLoader

ARTIFACTS_DIR = "artifacts"
RESUME_DIR = os.path.join(ARTIFACTS_DIR, "raw_resumes")
JD_DIR = os.path.join(ARTIFACTS_DIR, "raw_jds")

os.makedirs(RESUME_DIR, exist_ok=True)
os.makedirs(JD_DIR, exist_ok=True)

def save_uploaded_file(file, is_resume=True):
    """Save uploaded file to artifacts/raw_resumes or raw_jds."""
    subdir = RESUME_DIR if is_resume else JD_DIR
    filepath = os.path.join(subdir, file.name)
    
    with open(filepath, "wb") as f:
        f.write(file.getbuffer())
    
    return filepath

def load_document(file_path: str):
    """Load content from PDF, DOCX, or TXT using LangChain loader."""
    loader = UnstructuredFileLoader(file_path)
    docs = loader.load()
    return docs
