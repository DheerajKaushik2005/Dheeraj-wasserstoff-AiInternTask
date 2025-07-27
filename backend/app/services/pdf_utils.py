# backend/services/pdf_utils.py

import os
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import fitz  # PyMuPDF

# Set Poppler and Tesseract paths (update if your paths are different)
poppler_path = r"C:\poppler\poppler-24.08.0\Library\bin"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a digital PDF using PyMuPDF (fitz).
    Returns plain text or empty string if failed.
    """
    if not os.path.exists(pdf_path):
        return ""
    try:
        doc = fitz.open(pdf_path)
        return "\n".join(page.get_text() for page in doc)
    except Exception as e:
        print(f"[PDF Extract Error] {e}")
        return ""

def extract_text_with_ocr(pdf_path):
    """
    Extract text from a scanned PDF using OCR (Tesseract).
    Converts PDF pages to images and applies OCR.
    Returns extracted text.
    """
    try:
        images = convert_from_path(pdf_path, poppler_path=poppler_path)
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"
        return text
    except Exception as e:
        print(f"[OCR Extract Error] {e}")
        return ""
