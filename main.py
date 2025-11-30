from fastapi import FastAPI, HTTPException
import cv2 as cv
import requests
import numpy as np
import utils
from dotenv import load_dotenv
import os
from pdf2image import convert_from_bytes
from io import BytesIO

app = FastAPI()

load_dotenv()
api_key = os.getenv("API_KEY")

@app.get("/")
def home():
    return {"message": "Hello, this is my API!"}

@app.get("/add")
def add(document: str):
    try:
        if not api_key:
            raise HTTPException(status_code=500, detail="API_KEY not found in environment variables")
        
        http_response = requests.get(document)
        
        # Check if the link is a PDF or image
        if document.lower().endswith('.pdf'):
            # Convert PDF to images
            pdf_images = convert_from_bytes(http_response.content)
            if not pdf_images:
                raise ValueError("Failed to convert PDF to images")
            
            # Process all pages
            all_pages_data = []
            for page_num, pdf_image in enumerate(pdf_images, 1):
                img = cv.cvtColor(np.array(pdf_image), cv.COLOR_RGB2BGR)
                extracted_text = utils.extract_text_from_image(img)
                page_data = {
                    "page_no": page_num,
                    "extracted_text": extracted_text
                }
                all_pages_data.append(page_data)
            
            gemini_response = utils.structure_with_gemini(all_pages_data, api_key, is_multipage=True)
        else:
            # Handle as image file
            img_array = np.frombuffer(http_response.content, np.uint8)
            img = cv.imdecode(img_array, cv.IMREAD_COLOR)
            
            if img is None:
                raise ValueError("Failed to decode image data")
            
            extracted_text = utils.extract_text_from_image(img)
            gemini_response = utils.structure_with_gemini(extracted_text, api_key, is_multipage=False)
        
        output = utils.format_response(gemini_response)
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    # uvicorn.run(app, host="0.0.0.0", port=port)