# ---- Dockerfile ----------------------------------------------------------------
# Use an official slim Python image
FROM python:3.11-slim

# Prevents python from writing .pyc files and buffers stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app
ENV PORT=8000

# Set workdir
WORKDIR $APP_HOME

# Install system dependencies required for OCR/PDF processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    ca-certificates \
    curl \
    wget \
    # Tesseract OCR + libraries
    tesseract-ocr \
    libtesseract-dev \
    # cleaning
    && rm -rf /var/lib/apt/lists/*

# (Optional) Install additional language packs if needed, e.g. Hindi, Spanish:
# RUN apt-get update && apt-get install -y tesseract-ocr-spa tesseract-ocr-hin && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better caching
COPY requirements.txt .

# Upgrade pip then install Python deps
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Create a non-root user (recommended for security)
RUN useradd --create-home appuser && chown -R appuser:appuser $APP_HOME
USER appuser

# Expose port
EXPOSE ${PORT}

# Healthcheck (optional)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:${PORT}/docs || exit 1

# Start the app with uvicorn (use your module path if different)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
# --------------------------------------------------------------------------------