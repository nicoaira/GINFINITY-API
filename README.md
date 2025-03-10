# GINFINITY API

This repository hosts an API for generating embeddings of RNA secondary structures and computing similarity scores using GINFINITY model.

## Features
- Generate embeddings from RNA structures.
- Compare two RNA structures and compute a similarity score.
- API built using **FastAPI** (or Flask).
- **Dockerized** for easy deployment.
- **AWS-ready** (but works locally by default).

## 📂 Directory Structure
```
rna-similarity-api/
│── api/
│   ├── main.py              # Entry point
│   ├── models.py            # Model loading logic
│   ├── schemas.py           # Request validation
│   ├── routes/
│   │   ├── embeddings.py     # Embedding generation
│   │   ├── similarity.py     # Similarity calculation
│   │   ├── health.py         # Health check
│   ├── utils/
│   │   ├── preprocess.py     # RNA preprocessing
│   │   ├── postprocess.py    # Post-processing embeddings
│── tests/                    # Unit tests
│── notebooks/                 # Jupyter Notebooks
│── config/
│   ├── settings.py           # Configuration (Local/AWS settings)
│── docker/
│   ├── Dockerfile            # Containerization setup
│── models/                   # Model weights (local)
│── scripts/
│   ├── download_weights.py   # Script to fetch AWS model weights (optional)
│── .env                      # Environment variables
│── requirements.txt          # Dependencies
│── .gitignore                # Ignore unwanted files
│── docker-compose.yml        # Docker setup
│── .github/
│   ├── workflows/
│   │   ├── deploy.yml        # GitHub Actions CI/CD pipeline
```

## 🛠 Setup
Run the following to install dependencies and start the API locally:

```bash
pip install -r requirements.txt
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

To build and run the **Dockerized API**:
```bash
docker build -t ginfinity-api .
docker run -p 8000:8000 --env-file .env ginfinity-api
```

## Deployment
This API is **AWS-ready**. To deploy with AWS, just update  with your AWS S3 bucket and model weight location.

