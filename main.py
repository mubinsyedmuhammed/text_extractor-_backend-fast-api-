from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from PIL import Image
import pytesseract
import os
import re

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware (allows frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Dynamically detect Tesseract-OCR path (for portability)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TESSERACT_PATH = os.path.join(BASE_DIR, "Tesseract-OCR", "tesseract.exe")
if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
else:
    raise FileNotFoundError("Tesseract-OCR not found! Place it inside the project folder.")

# pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR/tesseract.exe"

# Function to clean extracted text
def clean_extracted_text(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9.,\n]\s\\]", "", text)   
    # text = text.strip()
    return text

# API route for text extraction
@app.post("/extract_text/")
async def extract_text(file: UploadFile = File(...)):
    try:
        # Read image bytes
        image_bytes = await file.read()
        image = Image.open(BytesIO(image_bytes))

        # Extract text using PyTesseract
        extracted_text = pytesseract.image_to_string(image)
        cleaned_text = clean_extracted_text(extracted_text).lower().title()

        return {"extracted_cleaned_text": cleaned_text}
    
    except Exception as e:
        return {"error": str(e)}

