# KYC Verification System

A modern Know Your Customer (KYC) verification system that validates user-submitted information against identification documents using AI-powered document analysis.

## Overview

This project consists of two main components:

- A React frontend for document upload and user information submission
- A FastAPI backend that processes documents and validates information using the Fireworks AI API

### Features

- Document upload and processing
- Real-time validation feedback
- Modern, responsive UI
- AI-powered document analysis
- Robust error handling and retries
- Comprehensive logging

## Project Structure

```
kyc-project/
├── kyc-frontend/          # React frontend application
│   ├── src/
│   ├── package.json
│   └── README.md         # Frontend-specific documentation
│
├── kyc_project/          # Python backend application
│   ├── main.py          # FastAPI application
│   ├── kyc_validator.py # Validation logic
│   ├── requirements.txt
│   └── README.md        # Backend-specific documentation
│
└── README.md            # This file
```

## Quick Start

### Prerequisites

- Node.js (v14.0.0 or higher)
- Python 3.8 or higher
- Fireworks API key
- npm (v6.0.0 or higher)

### Backend Setup

1. Navigate to the backend directory:

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

4. Start the server:

```bash
python main.py
```

The backend API will be available at `http://localhost:8000`

### Frontend Setup

1. Open a new terminal and navigate to the frontend directory:

```bash
cd kyc-frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Usage

1. Upload an identification document (passport or driver's license)
2. Fill in the personal information:
   - Full Name
   - Date of Birth
   - Address
3. Submit for verification
4. View the validation results

## Architecture

### Frontend

- Built with React and Vite
- Styled with Tailwind CSS
- Real-time feedback and error handling
- Responsive design for all devices

### Backend

- FastAPI for high-performance API
- Fireworks AI for document analysis

### Data Flow

1. User submits form with document and information
2. Frontend sends data to backend API
3. Backend processes document using Fireworks AI
4. Backend validates user information against document data
5. Results are returned to frontend
6. User sees validation results
