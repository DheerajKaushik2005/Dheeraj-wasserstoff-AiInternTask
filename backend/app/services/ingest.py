import os
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import fitz  # PyMuPDF

# This script processes image and PDF files to extract text and save it to text files.
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def process_files(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        full_path = os.path.join(input_dir, filename)

        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            text = extract_text_from_image(full_path)

        elif filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(full_path)

        else:
            continue

        if text.strip():
            out_file = os.path.join(output_dir, filename + ".txt")
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(text.strip())