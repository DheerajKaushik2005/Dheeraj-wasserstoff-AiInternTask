import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")
index = None
chunks = []

def embed_and_store_text(text: str):
    global index, chunks
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    embeddings = model.encode(chunks)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

def answer_question(query: str) -> str:
    if index is None:
        return "[ERROR] No index loaded."
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), k=1)
    return chunks[I[0][0]]
