# KYC Verification Backend

This is the backend API for the KYC (Know Your Customer) verification system. It processes identification documents and validates user information using the Fireworks AI API.

## Features

- Document processing using Vision AI
- User information validation
- CORS support for frontend integration
- Error handling and retries
- Temporary file management
- Logging system

## Prerequisites

- Python 3.8 or higher
- A Fireworks API key
- Virtual environment management tool (venv or conda)

## Installation

1. Clone the repository and navigate to the backend directory:

```bash
cd kyc_project
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## API Endpoints

### POST /validate

Validates user information against an uploaded identification document.

**Request:**

- Method: POST
- Content-Type: multipart/form-data
- Parameters:
  - `file`: Image file (JPG/PNG)
  - `name`: User's full name
  - `dob`: Date of birth
  - `address`: User's address

**Response:**

```json
{
  "status": "success",
  "validation_result": {
    "Result": "pass|fail",
    "Feedback": "reason for failure or 'none'"
  },
  "document_data": {
    "DOB": "...",
    "LN": "...",
    "FN": "..."
    // ... other document fields
  }
}
```

## Running the Server

1. Start the server:

```bash
python main.py
```

2. The API will be available at `http://localhost:8000`

3. API documentation is available at:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`
