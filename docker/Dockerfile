# Use Python as base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy source files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (AWS placeholders)
ENV MODEL_PATH=/app/models/model_weights.pth
ENV AWS_BUCKET_NAME=""
ENV AWS_MODEL_KEY="model_weights.pth"

# Download model from AWS **only if AWS_BUCKET_NAME is set**
ARG ENVIRONMENT=development
RUN if [ "$ENVIRONMENT" = "production" ] && [ -n "$AWS_BUCKET_NAME" ]; then \
        apt-get update && apt-get install -y curl && \
        curl -o $MODEL_PATH https://your-cloud-storage.com/model_weights.pth; \
    fi

# Expose API port
EXPOSE 8000

# Start the API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
