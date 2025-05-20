from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

bge_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}  # important for cosine similarity
)

embeddings = bge_model

def load_texts(text_dir):
    docs = []
    for filename in os.listdir(text_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(text_dir, filename), "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    docs.append(Document(page_content=content, metadata={"source": filename}))
    return docs

def embed_documents(docs, persist_dir="data/chroma_store"):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    chunks = [c for c in chunks if c.page_content.strip()]
    db = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=persist_dir)
    return db