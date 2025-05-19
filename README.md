# Email Classification and PII Masking API

This FastAPI application provides an API for classifying emails and masking Personally Identifiable Information (PII) in text.

## Features

- PII Detection and Masking
  - Full names
  - Email addresses
  - Phone numbers
  - Dates of birth
  - Aadhar numbers
  - Credit/Debit card numbers
  - CVV numbers
  - Card expiry dates
- Email Classification using MLP model
- Multilingual support using BERT-based models

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download required model files:
- `label_encoder.pkl`
- `pca.pkl`
- `mlp_model.pth`

## Usage

1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. The API will be available at `http://localhost:8000`

3. API Endpoints:
   - POST `/classify`: Classify and mask PII in email text
     - Input: JSON with `input_email_body` field
     - Output: JSON with masked text, detected entities, and classification

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
.
├── README.md
├── requirements.txt
├── main.py              # FastAPI application entry point
├── models.py            # ML model definitions and training logic
├── utils.py            # Utility functions for text processing
├── label_encoder.pkl   # Label encoder for classification
├── pca.pkl            # PCA model for dimensionality reduction
└── mlp_model.pth      # Trained MLP model weights
``` 