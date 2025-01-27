from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from PIL import Image
import pytesseract

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. You can specify specific origins here.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Path to the Tesseract executable (adjust according to your setup)
pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR/tesseract.exe"

@app.post("/extract_text/")
async def extract_text(file: UploadFile = File(...)):
    # Read the image from the incoming file
    image_bytes = await file.read()
    image = Image.open(BytesIO(image_bytes))

    # Extract text using pytesseract
    extracted_text = pytesseract.image_to_string(image)

    # Return the extracted text
    return {"extracted_cleaned_text": extracted_text}
