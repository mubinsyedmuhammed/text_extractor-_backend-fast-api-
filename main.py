from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
from io import BytesIO
import numpy  as np
import cv2

pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR/tesseract.exe'
app = FastAPI()

class TextCleaner():
    
    def __init__(self, text):
        self._original_text = text
        self._cleaned_text = self._clean_text(text)
    
    def _clean_text(self, text):
        
        text = text.replace("\n", ' ')
        return " ".join(text.split())

    def get_cleaned_text(self):
        
        return self._cleaned_text
            
    def get_original_text(self):
        
        return self._original_text
        

@app.post("/extract_text/")
async def extract_text(
    image: UploadFile = File(...),
    x: int = Form(...),
    y: int = Form(...),
    width: int = Form(...),
    height: int = Form(...)
):
    try:
        
        
        image_data = await image.read()
        pil_image = Image.open(BytesIO(image_data))
        
        # gray_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_BGR2GRAY)
             
        cropped_image = pil_image.crop((x, y, x + width, y + height))

        extracted_text = pytesseract.image_to_string(cropped_image)
        
        text_object = TextCleaner(extracted_text)
        
        original_extracted_text = text_object.get_original_text()
        cleaned_extracted_text = text_object.get_cleaned_text()
            
        return JSONResponse(content={
            "extracted_original_text": original_extracted_text,
            "extracted_cleaned_text": cleaned_extracted_text.strip()
        })

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

