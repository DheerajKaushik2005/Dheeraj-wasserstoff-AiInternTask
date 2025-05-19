import os
from dotenv import load_dotenv

# LangChain modern imports
from langchain_chroma import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.runnables import RunnableMap


embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load text files and clean them
def load_documents_from_folder(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            print(f"📁 Found file: {file_path}")

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                print(f"📝 Original length: {len(text)}")

                # Remove blank lines
                cleaned_text = text.strip()
                print(f"🧹 Cleaned length: {len(cleaned_text)}")

                if cleaned_text:
                    documents.append(Document(
                        page_content=cleaned_text,
                        metadata={"source": filename}
                    ))
                else:
                    print("⚠️ Skipped empty document")
    return documents


# Split documents into chunks
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    print(f"📄 Documents loaded: {len(documents)}")

    for i, doc in enumerate(documents):
        print(f"\n🧾 Document {i+1} ({doc.metadata['source']}): {repr(doc.page_content[:100])}")

    chunks = splitter.split_documents(documents)

    # Show all chunks before filtering
    print(f"📦 Chunks before filtering: {len(chunks)}")

    filtered_chunks = [chunk for chunk in chunks if chunk.page_content.strip()]
    print(f"✅ Total Documents Used as Chunks: {len(filtered_chunks)}")
    
    return filtered_chunks


# Create vector store
def create_vector_store(chunks, persist_directory="data/chroma_store"):
    if not chunks:
        print("❌ No valid chunks to embed. Aborting.")
        return

    print(f"🧠 Embedding {len(chunks)} chunks...")
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1}: {repr(chunk.page_content[:100])}...")

    try:
        vectordb = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=persist_directory)
        print("✅ Vector store created and saved.")
        return vectordb
    except Exception as e:
        print("❌ Failed to create Chroma vector store:", e)

# Query the store
from transformers import pipeline

qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

from langchain_community.llms import Ollama
from langchain.chains.question_answering import load_qa_chain



llm = OllamaLLM(model="mistral:7b-instruct", temperature=0.2)

prompt_template = PromptTemplate.from_template(
    """You are a helpful assistant.

Answer the question in ONE short sentence based only on the context provided. 
Ignore unrelated information. Be concise.

Context:
{context}

Question:
{question}

Answer:"""
)

# Prompt | Model as a pipeline
chain = prompt_template | llm

def ask_question(query, persist_directory="data/chroma_store"):
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    retriever = vectordb.as_retriever()
    docs = retriever.invoke(query)

    if not docs:
        return "⚠️ No relevant documents found."

    context = "\n".join([doc.page_content for doc in docs[:3]])

    result = chain.invoke({
        "context": context,
        "question": query
    })

    # Strip leading/trailing spaces and return clean one-liner
    return result.strip()



# Main
if __name__ == "__main__":
    folder = "data/text_outputs"
    print("📄 Loading documents...")
    docs = load_documents_from_folder(folder)

    print("🔗 Splitting into chunks...")
    chunks = split_documents(docs)

    print("📦 Creating vector store...")
    create_vector_store(chunks)

    print("✅ Ready! Ask a question (type 'exit' to quit):")
    while True:
        query = input("🔍 Your question: ")
        if query.lower() in ["exit", "quit"]:
            break
        answer = ask_question(query)
        print(f"🤖 {answer}")
