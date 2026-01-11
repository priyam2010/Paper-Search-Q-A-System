from backend.ingestion.paper_ingestor import ingest_paper
from backend.indexing.chunk_builder import build_chunks
from backend.indexing.faiss_index import FAISSIndex

paper = ingest_paper("data/standard-treatment-guidelines.pdf")
chunks = build_chunks(paper)

faiss_index = FAISSIndex()
faiss_index.index_papers(chunks)
faiss_index.save("faiss_store")

print("✅ FAISS index built and saved")
