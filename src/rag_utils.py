import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import faiss
import os
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
index_path = "vector_store/index.faiss"
texts_path = "vector_store/chunks.txt"

os.makedirs("vector_store", exist_ok=True)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join([page.get_text() for page in doc])

def chunk_text(text, chunk_size=300):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def ingest_document(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    embeddings = model.encode(chunks)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    faiss.write_index(index, index_path)

    with open(texts_path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk + "\n")

def query_vector_db(query, k=5):
    if not os.path.exists(index_path):
        return ["No data available"]

    index = faiss.read_index(index_path)
    with open(texts_path, "r", encoding="utf-8") as f:
        chunks = f.read().splitlines()

    query_embedding = model.encode([query])
    _, I = index.search(np.array(query_embedding), k)
    return [chunks[i] for i in I[0]]
