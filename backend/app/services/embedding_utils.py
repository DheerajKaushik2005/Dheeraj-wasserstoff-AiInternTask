from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings_from_text(text, chunk_size=300):
    """
    Split text into chunks and generate embeddings for each chunk.
    """
    chunks = []
    current = ""
    for line in text.split("\n"):
        if len(current) + len(line) < chunk_size:
            current += line + " "
        else:
            chunks.append(current.strip())
            current = line + " "
    if current:
        chunks.append(current.strip())

    embeddings = model.encode(chunks)
    return chunks, embeddings
