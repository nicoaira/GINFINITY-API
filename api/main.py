from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import torch
from api.models import load_model  # This is your model-loading code adapted for the API
from src.utils import validate_structure  # Utility to check valid dot-bracket strings
from predict_embedding import get_gin_embedding  # Reuse your embedding function
import os

# Initialize FastAPI app
app = FastAPI(title="RNA Similarity API")

# Set device and load model once on startup
device = "cuda" if torch.cuda.is_available() else "cpu"
model = load_model(model_path=os.getenv("MODEL_PATH", "models/model_weights.pth"), device=device)
graph_encoding = model.metadata.get('graph_encoding', "standard")  # Use default if not set

# --- Pydantic Models for Request and Response ---

class EmbedRequest(BaseModel):
    structure: str = Field(..., description="RNA secondary structure in dot-bracket notation")
    # Optional parameters for subgraph embedding generation:
    subgraphs: bool = False
    L: int = None
    keep_paired_neighbors: bool = False

class EmbedResponse(BaseModel):
    embeddings: list[str] = Field(..., description="List of embedding vectors as comma-separated floats")

class CompareRequest(BaseModel):
    structure1: str = Field(..., description="First RNA secondary structure in dot-bracket notation")
    structure2: str = Field(..., description="Second RNA secondary structure in dot-bracket notation")
    subgraphs: bool = False
    L: int = None
    keep_paired_neighbors: bool = False

class CompareResponse(BaseModel):
    similarity_score: float = Field(..., description="Squared Euclidean distance between embeddings")


# --- API Endpoints ---

@app.post("/embed", response_model=EmbedResponse)
def embed(request: EmbedRequest):
    try:
        # Validate input structure
        validate_structure(request.structure)
        # Get embedding(s) using your helper function.
        # This function returns a list of tuples (start_idx, embedding_string).
        emb_list = get_gin_embedding(
            model,
            graph_encoding,
            request.structure,
            device,
            L=request.L,
            keep_paired_neighbors=request.keep_paired_neighbors
        )
        # For simplicity, if subgraphs is False, use the first (or only) embedding.
        embeddings = [emb for _, emb in emb_list]
        return EmbedResponse(embeddings=embeddings)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/compare", response_model=CompareResponse)
def compare(request: CompareRequest):
    try:
        # Validate both input structures
        validate_structure(request.structure1)
        validate_structure(request.structure2)
        
        # Generate embeddings for each structure
        emb_list1 = get_gin_embedding(
            model,
            graph_encoding,
            request.structure1,
            device,
            L=request.L,
            keep_paired_neighbors=request.keep_paired_neighbors
        )
        emb_list2 = get_gin_embedding(
            model,
            graph_encoding,
            request.structure2,
            device,
            L=request.L,
            keep_paired_neighbors=request.keep_paired_neighbors
        )
        # For simplicity, use the first embedding from each list.
        emb_str1 = emb_list1[0][1]
        emb_str2 = emb_list2[0][1]

        # Convert comma-separated string to float list
        def parse_embedding(emb_str):
            return [float(x) for x in emb_str.split(',')]
        vec1 = parse_embedding(emb_str1)
        vec2 = parse_embedding(emb_str2)

        # Compute squared Euclidean distance
        if len(vec1) != len(vec2):
            raise ValueError("Embedding dimensions do not match.")
        distance = sum((x - y) ** 2 for x, y in zip(vec1, vec2))
        return CompareResponse(similarity_score=distance)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
