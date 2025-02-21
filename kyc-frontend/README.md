# KYC Verification Frontend

This is the frontend application for the KYC (Know Your Customer) verification system. It provides a modern, user-friendly interface for submitting and validating identification documents.

## Prerequisites

Before you begin, ensure you have installed:

- Node.js (v14.0.0 or higher)
- npm (v6.0.0 or higher)

The backend server should be running on `http://localhost:8000`. See the backend README for setup instructions.

## Installation

1. Clone the repository and navigate to the frontend directory:

```bash
cd kyc-frontend
```

2. Install dependencies:

```bash
npm install
```

## Running the Application

1. Start the development server:

```bash
npm run dev
```

2. The application will be available at `http://localhost:5173`

## Usage

1. Fill in the required personal information:

   - Full Name
   - Date of Birth
   - Address

2. Upload an identification document (supported formats: JPG, PNG)

   - Either drag and drop the file or click to select
   - Maximum file size: 10MB

3. Click "Verify Identity" to submit

4. View the verification results:
   - Pass/Fail status
   - Detailed feedback if verification fails
   - Document data extracted from the ID
