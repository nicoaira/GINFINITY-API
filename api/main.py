from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import os
import torch
from typing import Union, List  # removed Optional since no longer needed for L

# Import shared functions and model loader
from api.models import load_model
from api.utils.embedding import get_gin_embedding
from external.GINFINITY.src.utils import is_valid_dot_bracket as validate_structure
from external.GINFINITY.src.utils import calculate_distances

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
    # Removed subgraphs, L, and keep_paired_neighbors

class EmbedResponse(BaseModel):
    embeddings: list[str] = Field(..., description="List of embedding vectors (as comma-separated floats)")

class CompareRequest(BaseModel):
    structure1: str = Field(..., description="First RNA secondary structure in dot-bracket notation")
    structure2: Union[str, List[str]] = Field(..., description="Second RNA structure(s) in dot-bracket notation")
    metric: str = Field("squared", description="Distance metric: 'squared' or 'cosine'")
    # Removed subgraphs, L, and keep_paired_neighbors

class CompareResponse(BaseModel):
    similarity_score: Union[float, List[float]] = Field(..., description="Similarity score(s) between embeddings")

# Endpoint to generate embedding(s) for a given RNA structure
@app.post("/embed", response_model=EmbedResponse)
def embed_endpoint(request: EmbedRequest):
    try:
        validate_structure(request.structure)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    try:
        # Removed extra parameters: now call with only structure and device.
        emb_list = get_gin_embedding(
            model,
            graph_encoding,
            request.structure,
            device
        )
        embeddings = [emb for _, emb in emb_list]
        return EmbedResponse(embeddings=embeddings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error computing embedding: {str(e)}")

# Endpoint to compare two RNA structures
@app.post("/compare", response_model=CompareResponse)
def compare_endpoint(request: CompareRequest):
    try:
        validate_structure(request.structure1)
        if isinstance(request.structure2, list):
            for s in request.structure2:
                validate_structure(s)
        else:
            validate_structure(request.structure2)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    try:
        emb_list1 = get_gin_embedding(
            model,
            graph_encoding,
            request.structure1,
            device
        )
        emb_str1 = emb_list1[0][1]
        vec1 = [float(x) for x in emb_str1.split(',')]
        
        def compute_similarity(vec_a, vec_b, metric):
            embeddings = [vec_a, vec_b]
            distances = calculate_distances(embeddings, metric=metric, num_workers=1, batch_size=1)
            return distances[0][2]
        
        if isinstance(request.structure2, list):
            scores = []
            for s in request.structure2:
                emb_list2 = get_gin_embedding(
                    model,
                    graph_encoding,
                    s,
                    device
                )
                emb_str2 = emb_list2[0][1]
                vec2 = [float(x) for x in emb_str2.split(',')]
                if len(vec1) != len(vec2):
                    raise HTTPException(status_code=400, detail="Embedding dimensions do not match.")
                scores.append(compute_similarity(vec1, vec2, request.metric))
            return CompareResponse(similarity_score=scores)
        else:
            emb_list2 = get_gin_embedding(
                model,
                graph_encoding,
                request.structure2,
                device
            )
            emb_str2 = emb_list2[0][1]
            vec2 = [float(x) for x in emb_str2.split(',')]
            if len(vec1) != len(vec2):
                raise HTTPException(status_code=400, detail="Embedding dimensions do not match.")
            score = compute_similarity(vec1, vec2, request.metric)
            return CompareResponse(similarity_score=score)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error computing similarity: {str(e)}")
