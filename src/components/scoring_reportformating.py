import os
import requests
from typing import List, Dict
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from dotenv import load_dotenv
import logging

load_dotenv()

# ---------------------------
# Prompt Templates
# ---------------------------

SWOT_PROMPT = """
You are an HR expert and resume analyst. Based on the following resume chunks and job description, generate a detailed SWOT analysis.

Resume Chunks:
{resume_chunks}

Job Description:
{job_description}

Return your response as:
Strengths:
Weaknesses:
Opportunities:
Threats:
"""

ATS_PROMPT = """
You are an ATS evaluator. Based on the resume and job description below, give an ATS score (0–100) and describe why.

Resume:
{resume_chunks}

Job Description:
{job_description}

Return format:
ATS Score: X/100
Reasoning:
"""

SUGGESTION_PROMPT = """
You're a resume improvement expert. Given the resume and JD below, suggest changes to make the resume better match the JD.

Resume:
{resume_chunks}

Job Description:
{job_description}

Suggestions:
1. ...
2. ...
"""

# ---------------------------
# Resume Merger
# ---------------------------

def merge_chunks(chunks: List[Document], max_tokens: int = 1500) -> str:
    content = ""
    for chunk in chunks:
        if len(content) + len(chunk.page_content) < max_tokens * 4:
            content += chunk.page_content + "\n"
        else:
            break
    return content.strip()


# ---------------------------
# Mistral API Client
# ---------------------------

class MistralLLMClient:
    def __init__(self):
        self.api_url = "https://api.mistral.ai/v1/chat/completions"
        self.api_key = self._get_api_key()

        if not self.api_key:
            raise ValueError("Mistral API key not found")

        logging.debug("✅ Mistral API key loaded successfully")

    def _get_api_key(self) -> str:
        key_sources = [
            self._get_key_from_env_vars,
            self._get_key_from_streamlit,
            self._get_key_from_file
        ]
        for source in key_sources:
            try:
                api_key = source()
                if api_key:
                    return api_key
            except Exception as e:
                logging.warning(f"Failed to get API key from {source.__name__}: {str(e)}")
        return None

    def _get_key_from_env_vars(self) -> str:
        return os.getenv("MISTRAL_API_KEY")

    def _get_key_from_streamlit(self) -> str:
        import streamlit as st
        return st.secrets["MISTRAL_API_KEY"] if "MISTRAL_API_KEY" in st.secrets else None

    def _get_key_from_file(self) -> str:
        path = os.path.expanduser("~/.mistral_api_key")
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read().strip()
        return None

    def generate_response(self, system_prompt: str, user_prompt: str, model="mistral-small-latest", temperature=0.3) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }

        response = requests.post(self.api_url, headers=headers, json=payload)
        if response.status_code != 200:
            raise RuntimeError(f"Mistral API Error: {response.status_code} - {response.text}")

        return response.json()["choices"][0]["message"]["content"]


# ---------------------------
# Report Functions
# ---------------------------

def generate_swot(resume_chunks: List[Document], jd_text: str, model="mistral-small-latest") -> str:
    llm = MistralLLMClient()
    template = PromptTemplate.from_template(SWOT_PROMPT)
    merged = merge_chunks(resume_chunks)
    prompt = template.format(resume_chunks=merged, job_description=jd_text)
    return llm.generate_response("You are an HR expert.", prompt, model=model)


def generate_ats_score(resume_chunks: List[Document], jd_text: str, model="mistral-small-latest") -> str:
    llm = MistralLLMClient()
    template = PromptTemplate.from_template(ATS_PROMPT)
    merged = merge_chunks(resume_chunks)
    prompt = template.format(resume_chunks=merged, job_description=jd_text)
    return llm.generate_response("You are an ATS evaluator.", prompt, model=model)


def generate_improvement_suggestions(resume_chunks: List[Document], jd_text: str, model="mistral-small-latest") -> str:
    llm = MistralLLMClient()
    template = PromptTemplate.from_template(SUGGESTION_PROMPT)
    merged = merge_chunks(resume_chunks)
    prompt = template.format(resume_chunks=merged, job_description=jd_text)
    return llm.generate_response("You are a resume improvement assistant.", prompt, model=model)


def generate_full_report(resume_chunks: List[Document], jd_text: str, model="mistral-small-latest") -> Dict[str, str]:
    return {
        "SWOT_Analysis": generate_swot(resume_chunks, jd_text, model),
        "ATS_Score": generate_ats_score(resume_chunks, jd_text, model),
        "Suggestions": generate_improvement_suggestions(resume_chunks, jd_text, model)
    }
