import os
import boto3
from config.settings import MODEL_PATH, AWS_BUCKET_NAME, AWS_MODEL_KEY

def download_model_from_s3():
    """Download model weights from AWS S3."""
    if AWS_BUCKET_NAME:
        print(f"Downloading model from S3: {AWS_BUCKET_NAME}/{AWS_MODEL_KEY}...")
        s3 = boto3.client("s3")
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        s3.download_file(AWS_BUCKET_NAME, AWS_MODEL_KEY, MODEL_PATH)
        print("Download complete!")

if __name__ == "__main__":
    download_model_from_s3()
