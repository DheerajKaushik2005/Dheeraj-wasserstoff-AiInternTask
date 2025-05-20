from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableMap
from langchain_chroma import Chroma
from backend.app.services.embed import embeddings

llm = OllamaLLM(model="gemma:2b", temperature=0.2)

prompt = PromptTemplate.from_template(
    """You are a helpful assistant.

Based on the context below, answer the question in a short sentence.
If the user asks about experience or qualifications, focus on the context and check for relevant information.
If the user asks about a specific topic, provide a brief summary.
If the user asks for a definition, provide a concise definition.
If the user asks for a list, provide a short list.
If the answer is clearly stated, use it. If not, make an informed guess if possible.

Context:
{context}

Question:
{question}

Answer:"""
)


chain = prompt | llm

def ask_question(query, persist_dir="data/chroma_store"):
    db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 6})
    docs = retriever.invoke(query)
    if not docs:
        return "⚠️ No relevant documents found."
    context = "\n".join([doc.page_content for doc in docs])
    return chain.invoke({"context": context, "question": query}).strip()