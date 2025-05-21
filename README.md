---
title: Email Classification and PII Masking API
emoji: 📧
colorFrom: blue
colorTo: purple
sdk: dockerfile
sdk_version: "latest"
app_file: main.py
pinned: false
models:
  - Davlan/bert-base-multilingual-cased-ner-hrl
  - sentence-transformers/paraphrase-multilingual-mpnet-base-v2
---

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

2.  Install dependencies:

```bash
pip install -r requirements.txt
```

3.  Download required model files:

  - `label_encoder.pkl`
  - `pca.pkl`
  - `mlp_model.pth`
    Place these files in the same directory as `main.py`.

## Usage

1.  Start the FastAPI server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 7860
```

**Note for Hugging Face Spaces:** We explicitly bind to `0.0.0.0` and port `7860`, which is typically required by Spaces.

2.  The API will be available at the Space's URL (e.g., `https://your-username-your-space-name.hf.space`).

3.  API Endpoints:

  - **POST `/classify`**: Classify and mask PII in email text
      - **Input:** JSON with `input_email_body` field
```json
{
  "input_email_body": "Hello, my name is John Doe and my email is john.doe@example.com. Please help with my billing issue."
}
```
      - **Output:** JSON with masked text, detected entities, and classification
```json
{
  "input_email_body": "Hello, my name is John Doe and my email is john.doe@example.com. Please help with my billing issue.",
  "list_of_masked_entities": [
    {
      "position": [
        16,
        24
      ],
      "classification": "full_name",
      "entity": "John Doe"
    },
    {
      "position": [
        39,
        60
      ],
      "classification": "email",
      "entity": "john.doe@example.com"
    }
  ],
  "masked_email": "Hello, my name is [full_name] and my email is [email]. I'm having trouble with my account.",
  "category_of_the_email": "Issues"
}
```

## API Documentation

Once the server is running on Hugging Face Spaces, the Swagger UI and ReDoc documentation endpoints might not be directly accessible via the standard `/docs` and `/redoc` paths in a "Static" Space setup. You would typically interact with the `/classify` endpoint directly via POST requests.

## Project Structure

```
.
├── README.md
├── requirements.txt
├── main.py         # FastAPI application entry point
├── models.py       # ML model definitions and training logic
├── utils.py        # Utility functions for text processing
├── label_encoder.pkl # Label encoder for classification
├── pca.pkl         # PCA model for dimensionality reduction
└── mlp_model.pth   # Trained MLP model weights
```

## Deployment on Hugging Face Spaces

To deploy this application on Hugging Face Spaces:

1.  **Create a new Space** on [https://huggingface.co/spaces](https://huggingface.co/spaces).
2.  Choose a **Space name**, select a **license**, and for **Space Hardware**, the "Free" tier should be sufficient for this type of API.
3.  Crucially, under **SDK**, select **"Static"**.
4.  In your Space's settings, link your **GitHub repository** containing these files.
5.  Hugging Face Spaces will automatically detect the `requirements.txt` and install the dependencies.
6.  It will then look for an `app_file` specified in the frontmatter (`main.py` in this case) to run. For a "Static" Space running a FastAPI application, it will execute `uvicorn main:app --host 0.0.0.0 --port 7860`.

Ensure all your model files (`label_encoder.pkl`, `pca.pkl`, `mlp_model.pth`) are present in your repository at the root level or in the same directory as `main.py`.
