import os

# Use local model path by default
MODEL_PATH = os.getenv("MODEL_PATH", "models/model_weights.pth")

# AWS placeholders (for future use)
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", None)  # None means ignore AWS
AWS_MODEL_KEY = os.getenv("AWS_MODEL_KEY", "model_weights.pth")

# Example for local MySQL database (adjust these values as needed)
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "3306")
DATABASE_USER = os.getenv("DATABASE_USER",  default=None)
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", default=None)
DATABASE_NAME = os.getenv("DATABASE_NAME", "rna_db")

# Construct the connection URL for MySQL (using pymysql)
DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
