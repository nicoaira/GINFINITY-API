from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import os
import torch

# Import shared functions and model loader
from api.models import load_model
from api.utils.embedding import get_gin_embedding
from external.GINFINITY.src.utils import is_valid_dot_bracket as validate_structure # Assuming your shared utils include this

# Initialize FastAPI app
app = FastAPI(title="RNA Similarity API")

# Set device and load the model once at startup
device = "cuda" if torch.cuda.is_available() else "cpu"
# The model checkpoint path is taken from an environment variable or a default location
model_checkpoint = os.getenv("MODEL_PATH", "models/model_weights.pth")
model = load_model(model_checkpoint, device)
graph_encoding = model.metadata.get("graph_encoding", "standard")

# Define Pydantic models for input and output
class EmbedRequest(BaseModel):
    structure: str = Field(..., description="RNA secondary structure in dot-bracket notation")
    subgraphs: bool = False
    L: int = None
    keep_paired_neighbors: bool = False

class EmbedResponse(BaseModel):
    embeddings: list[str] = Field(..., description="List of embedding vectors (as comma-separated floats)")

class CompareRequest(BaseModel):
    structure1: str = Field(..., description="First RNA secondary structure in dot-bracket notation")
    structure2: str = Field(..., description="Second RNA secondary structure in dot-bracket notation")
    subgraphs: bool = False
    L: int = None
    keep_paired_neighbors: bool = False

class CompareResponse(BaseModel):
    similarity_score: float = Field(..., description="Squared Euclidean distance between embeddings")

# Endpoint to generate embedding(s) for a given RNA structure
@app.post("/embed", response_model=EmbedResponse)
def embed_endpoint(request: EmbedRequest):
    try:
        # Validate structure using your shared validation function
        validate_structure(request.structure)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    try:
        emb_list = get_gin_embedding(
            model,
            graph_encoding,
            request.structure,
            device,
            L=request.L,
            keep_paired_neighbors=request.keep_paired_neighbors
        )
        # Return all computed embeddings as a list of strings
        embeddings = [emb for _, emb in emb_list]
        return EmbedResponse(embeddings=embeddings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error computing embedding: {str(e)}")

# Endpoint to compare two RNA structures
@app.post("/compare", response_model=CompareResponse)
def compare_endpoint(request: CompareRequest):
    try:
        # Validate both structures
        validate_structure(request.structure1)
        validate_structure(request.structure2)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    try:
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
        # For simplicity, take the first embedding from each result
        emb_str1 = emb_list1[0][1]
        emb_str2 = emb_list2[0][1]
        
        # Convert the embedding strings into lists of floats
        vec1 = [float(x) for x in emb_str1.split(',')]
        vec2 = [float(x) for x in emb_str2.split(',')]
        
        if len(vec1) != len(vec2):
            raise HTTPException(status_code=400, detail="Embedding dimensions do not match.")
        
        # Compute squared Euclidean distance
        distance = sum((a - b) ** 2 for a, b in zip(vec1, vec2))
        return CompareResponse(similarity_score=distance)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error computing similarity: {str(e)}")
