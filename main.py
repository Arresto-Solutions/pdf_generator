from fastapi import FastAPI, Request
from pydantic import BaseModel, HttpUrl
from typing import Optional
import pdfkit
import requests

app = FastAPI()

class PDFRequest(BaseModel):
    html: str
    filename: str
    presigned_url: Optional[HttpUrl] = None  # Optional presigned URL for upload

@app.post("/generate-pdf")
def generate_pdf(request: PDFRequest):
    pdf = pdfkit.from_string(request.html, False)
    
    result = {
        "message": "PDF generated successfully"
    }
    
    # If presigned URL is provided, upload to it
    if request.presigned_url:
        try:
            response = requests.put(
                str(request.presigned_url), 
                data=pdf,
                headers={'Content-Type': 'application/pdf'}
            )
            if response.status_code == 200:
                result["url"] = str(request.presigned_url).split('?')[0]  # Base URL without query params
                result["message"] = "PDF generated and uploaded successfully"
            else:
                result["upload_error"] = f"Failed to upload to presigned URL: {response.status_code}"
        except Exception as e:
            result["upload_error"] = f"Error uploading to presigned URL: {str(e)}"

    return result
