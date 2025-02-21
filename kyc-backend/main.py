# main.py
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import tempfile
import os
from datetime import datetime

# Import your existing KYC validator
from kyc_validator import KYCValidator

# Initialize FastAPI app
app = FastAPI(title="KYC Validation API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React's default dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize the KYC validator with your API key
api_key = os.getenv('FIREWORKS_API_KEY')
validator = KYCValidator(api_key=api_key)

@app.post("/validate")
async def validate_kyc(
    file: UploadFile = File(...),
    name: str = Form(...),
    dob: str = Form(...),
    address: str = Form(...)
):
    """
    Endpoint to validate KYC documents against user-submitted information.
    """
    try:
        # Create temporary file to store the uploaded image
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            # Write uploaded file content to temporary file
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            # Prepare user data
            user_data = {
                "name": name,
                "dob": dob,
                "address": address
            }

            # Extract information from the document
            document_data = await validator.extract_document_info(temp_file_path)
            
            # Validate user data against document data
            validation_result = await validator.validate_user_data(user_data, document_data)

            # Clean up the temporary file
            os.unlink(temp_file_path)

            return {
                "status": "success",
                "validation_result": validation_result,
                "document_data": document_data
            }

        except Exception as e:
            # Clean up the temporary file in case of error
            os.unlink(temp_file_path)
            raise HTTPException(status_code=400, detail=f"Error processing document: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing request: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)