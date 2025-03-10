import os

# Use local model path by default
MODEL_PATH = os.getenv("MODEL_PATH", "models/model_weights.pth")

# AWS placeholders (for future use)
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", None)  # None means ignore AWS
AWS_MODEL_KEY = os.getenv("AWS_MODEL_KEY", "model_weights.pth")
