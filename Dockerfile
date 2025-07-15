# Use a slim Python base image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # for audio/video processing
    ffmpeg libsm6 libxext6 libgl1 \
    # for OCR
    tesseract-ocr \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python requirements
COPY requirements.txt .

# Install Python packages
RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt \ 
  && pip install detectron2

# Copy your backend code
COPY ./backend /app/backend

# Expose FastAPI port
EXPOSE 8000

# Default command: launch Uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
