

import os
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import fitz  # PyMuPDF
from fastapi import FastAPI, Body
from pydantic import BaseModel
from backend.app.services.main import answer_question_from_pdf

# Set up poppler path (adjust this to your extracted Poppler bin path)
poppler_path = r"C:\poppler\poppler-24.08.0\Library\bin"

# Configure Tesseract path for Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# FastAPI app and request model
app = FastAPI()

class QueryRequest(BaseModel):
    question: str
    file_path: str

def extract_text_from_image(image_path):
    """Extract text from an image file. Returns text or error message."""
    if not os.path.exists(image_path):
        return f"[ERROR] Image file not found: {image_path}"
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text.strip() if text.strip() else "[INFO] No text found in image."
    except Exception as e:
        return f"[ERROR] Failed to extract text from image: {e}"

# Main API endpoint

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file. Returns text or error message."""
    if not os.path.exists(pdf_path):
        return f"[ERROR] PDF file not found: {pdf_path}"
    try:
        doc = fitz.open(pdf_path)
        text = "".join(page.get_text() for page in doc)
        return text.strip() if text.strip() else "[INFO] No text found in PDF."
    except Exception as e:
        return f"[ERROR] Failed to extract text from PDF: {e}"

# Main API endpoint

# Main API endpoint
@app.post("/ask")
async def ask(request: QueryRequest):
    answer = answer_question_from_pdf(request.file_path, request.question)
    return {"answer": answer}


#this is command to run backend app
# To run the app, use the command below in your terminal:
#uvicorn backend.app.services.backend:app --reload









