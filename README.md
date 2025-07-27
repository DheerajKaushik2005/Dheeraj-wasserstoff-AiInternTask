# 📄 Document Research & Theme Identification Chatbot

This is an intelligent chatbot system that allows users to upload PDF/DOCX documents and ask natural language questions about them. The system extracts the text, identifies main themes, performs semantic search, and provides context-aware answers.

---

## 🚀 Features

-  Upload documents (PDF/DOCX)
- Extract and clean text from documents using OCR
-  Generate semantic embeddings with Sentence Transformers
-  Perform fast document search using FAISS vector search
-  Ask questions and get AI-generated answers with cited context
-  Identify and summarize main themes of the document
-  Web interface built using Streamlit

---

## 📁 Project Structure

Document-Research-Theme-Identification-Chatbot/
│
├── backend/ # Core logic and services
│ └── app/
│ └── services/ # Theme extraction, embedding, OCR
│
├── frontend/ # Streamlit app frontend
│ └── app.py # Main Streamlit interface
│
├── data/ # Uploaded files and processed data
├── temp/ # Temporary storage
│
├── main.py # Entry point (optional)
├── streamlit_app.py # Streamlit launcher
├── requirements.txt # Python dependencies
├── README.md # Project overv

🧠 How It Works
- Upload a document via the Streamlit interface.
- The backend extracts text (using PyMuPDF or Tesseract OCR).
- The document is split into chunks and converted to vector embeddings.
- User asks a question → the system converts it to a vector.
- nFAISS searches the most relevant chunks.
- The system returns answers and identifies key themes
 
  📚 Technologies Used
- Python
- Streamlit
- PyMuPDF / Tesseract OCR
- SentenceTransformers
- FAISS
- FastAPI (for backend, optional)
- OpenAI (optional for LLM-based answering)
  
 Example Questions
= What are the main points in the document?"
- "Summarize the report in 5 lines."
- "What does it say about climate change?"
- "Give 3 key findings from the uploaded research."



