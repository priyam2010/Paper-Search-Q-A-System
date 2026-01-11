import sys
import os
import streamlit as st

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)
sys.path.insert(0, PROJECT_ROOT)

from backend.ingestion.paper_ingestor import ingest_paper
from backend.indexing.chunk_builder import build_chunks
from backend.indexing.faiss_index import FAISSIndex
from backend.llm.groq_client import GroqLLM
from backend.rag.qa_pipeline import QAPipeline

UPLOAD_DIR = os.path.join(PROJECT_ROOT, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(page_title="Research Intelligence System", layout="wide")
st.title("📚 Research Intelligence System")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

@st.cache_resource(show_spinner=False)
def build_pipeline(pdf_path):
    paper_pages = ingest_paper(pdf_path)
    chunks = build_chunks(paper_pages)

    index = FAISSIndex()
    index.index_papers(chunks)

    llm = GroqLLM()
    return QAPipeline(index, llm)

if uploaded_file:
    pdf_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ PDF uploaded")

    with st.spinner("Indexing document..."):
        qa = build_pipeline(pdf_path)

    question = st.text_input("Ask a question")

    if question:
        result = qa.ask(question)

        st.subheader("Answer")
        st.write(result["answer"])

        st.subheader("Sources")
        st.text(result["sources"])
else:
    st.info("⬆️ Upload a PDF to begin")
