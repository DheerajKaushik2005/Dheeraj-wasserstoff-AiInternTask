import pytesseract
from PIL import Image
import os

# Set this only if you're on Windows and installed Tesseract manually
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

def process_folder(folder_path, output_path):
    for filename in os.listdir(folder_path):
        print(f"\nFound file: {filename}")
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            full_path = os.path.join(folder_path, filename)
            print(f"Processing: {full_path}")
            text = extract_text_from_image(full_path)
            print(f"Extracted text (first 200 chars): {text[:200]}")

            out_file = os.path.join(output_path, filename + ".txt")
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(text.encode("utf-8", errors="ignore").decode("utf-8"))
            print(f"Saved to {out_file}")
        else:
            print("Skipped (not an image)")



# Example usage:
if __name__ == "__main__":
    input_folder = "data/input_images"
    output_folder = "data/text_outputs"

    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    process_folder(input_folder, output_folder)