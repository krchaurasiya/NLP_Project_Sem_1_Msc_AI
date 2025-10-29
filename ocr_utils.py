from pdf2image import convert_from_path
import easyocr
import pytesseract
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

latin_reader = easyocr.Reader(['pt', 'en'], gpu=False)
devanagari_reader = easyocr.Reader(['hi', 'en'], gpu=False)

def extract_text_from_file(file_path, src_lang="en", mode="auto"):
    text = ""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        # Convert PDF pages to images
        pages = convert_from_path(file_path)
        for page in pages:
            if src_lang in ["pt", "en"]:
                text += " ".join(latin_reader.readtext(page, detail=0)) + " "
            elif src_lang == "hi":
                text += pytesseract.image_to_string(page, lang="hin+eng") + " "
    else:
        # For images
        if src_lang in ["pt", "en"]:
            text = " ".join(latin_reader.readtext(file_path, detail=0))
        elif src_lang == "hi":
            text = pytesseract.image_to_string(Image.open(file_path), lang="hin+eng")
    
    return text.strip()
