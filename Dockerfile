FROM python:3.11-slim

# Set working directory
WORKDIR /

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY api_server.py .
COPY utils/ ./utils/
COPY config/ ./config/
COPY setup.py .
COPY .env .
COPY credentials.json .
COPY README.md .
COPY n8n-workflows/ ./n8n-workflows/

# Create necessary directories
RUN mkdir -p logs data credentials

# Set environment variables
ENV PYTHONPATH=/
ENV FLASK_APP=api_server.py
ENV FLASK_ENV=production

# Google Drive API Configuration
ENV GOOGLE_DRIVE_CREDENTIALS_FILE=credentials.json

# OpenAI API Configuration
ENV GEMINI_API_KEY="AIzaSyBowvDLooKcTQyt2ioVg50OtD2JmHdH4k4"


# Twilio Configuration
ENV TWILIO_ACCOUNT_SID="ACa1111546e5db029e4b0c6526b7376487"
ENV TWILIO_AUTH_TOKEN="bdcb441a1613aebddd6ea4b24acf8d58"
ENV TWILIO_WHATSAPP_NUMBER="+14155238886"

# API Server Configuration
ENV API_SERVER_URL=https://localhost:5000


# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Run the application
CMD ["python", "api_server.py"]
