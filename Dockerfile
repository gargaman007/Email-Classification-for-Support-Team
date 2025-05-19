# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Prevent Python from writing .pyc files to disc and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install git (required by some HF models) and basic system tools
RUN apt-get update && apt-get install -y git && apt-get clean

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download NER model
RUN python -c "from transformers import AutoTokenizer, AutoModelForTokenClassification; \
               model = AutoModelForTokenClassification.from_pretrained('Davlan/bert-base-multilingual-cased-ner-hrl'); \
               tokenizer = AutoTokenizer.from_pretrained('Davlan/bert-base-multilingual-cased-ner-hrl'); \
               model.save_pretrained('./model'); tokenizer.save_pretrained('./model')"

# Pre-download SentenceTransformer model
RUN python -c "from sentence_transformers import SentenceTransformer; \
               model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2'); \
               model.save('./sbert_model')"

# Copy app code into container
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
