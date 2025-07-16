import streamlit as st
import os
import tempfile
from src.pipeline import run_resume_pipeline

st.set_page_config(page_title="📄 Resume Scanner", layout="wide")

st.title("📄 AI Resume & JD Analyzer")
st.markdown("Upload a resume and job description to get a detailed report: SWOT, ATS score, and improvement tips.")

# Upload widgets
resume_file = st.file_uploader("📎 Upload Resume", type=["pdf", "docx", "txt"])
jd_file = st.file_uploader("📎 Upload Job Description", type=["pdf", "docx", "txt"])

# Model selection
model_choice = st.selectbox(
    "🧠 Select Embedding Model (Ollama)",
    ["nomic-embed-text", "mxbai-embed-large", "all-minilm"],
    index=0
)

# Run button
if st.button("🚀 Analyze") and resume_file and jd_file:
    with st.spinner("Processing... This may take 30–60 seconds."):

        # Save uploaded files to temp paths
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(resume_file.name)[-1]) as tmp_resume:
            tmp_resume.write(resume_file.read())
            resume_path = tmp_resume.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(jd_file.name)[-1]) as tmp_jd:
            tmp_jd.write(jd_file.read())
            jd_path = tmp_jd.name

        # Run pipeline
        try:
            report = run_resume_pipeline(
                resume_path=resume_path,
                jd_path=jd_path,
                resume_index_name="resume_index",
                model_name=model_choice
            )

            # Display report
            st.success("✅ Analysis Complete!")

            with st.expander("🧠 SWOT Analysis", expanded=True):
                st.markdown(report["SWOT_Analysis"])

            with st.expander("📊 ATS Score", expanded=True):
                st.markdown(report["ATS_Score"])

            with st.expander("🔧 Suggestions", expanded=True):
                st.markdown(report["Suggestions"])

        except Exception as e:
            st.error(f"❌ Something went wrong: {str(e)}")

else:
    st.info("⬆️ Please upload both a resume and job description to begin.")
