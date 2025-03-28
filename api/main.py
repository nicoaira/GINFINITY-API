from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Response
from pydantic import BaseModel, Field
import os
import torch
from typing import Union, List
from sqlalchemy.orm import Session
import pandas as pd
import io

# Import shared functions and model loader
from api.models import load_model
from api.utils.embedding import get_gin_embedding, calculate_query_distances
from external.GINFINITY.src.utils import is_valid_dot_bracket as validate_structure
from external.GINFINITY.src.utils import calculate_distances

# Add database dependency and model import:
from db.connection import get_db
from db.models import Embedding

# Import health router
from api.routes import health

# Imports the StaticFiles class to serve static files
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import FileResponse

# Initialize FastAPI app and include API routes first
app = FastAPI(title="RNA Similarity API")
app.include_router(health.router)

# Mount static files on a dedicated subpath
app.mount("/frontend", StaticFiles(directory="ginfinity-frontend/dist", html=True), name="frontend")

# Set device and load the model once at startup
device = "cuda" if torch.cuda.is_available() else "cpu"
model_checkpoint = os.getenv("MODEL_PATH", "models/model_weights.pth")
model = load_model(model_checkpoint, device)
graph_encoding = model.metadata.get("graph_encoding", "standard")

# Define Pydantic models for input and output
class EmbedRequest(BaseModel):
    structure: str = Field(..., description="RNA secondary structure in dot-bracket notation")

class EmbedResponse(BaseModel):
    embeddings: list[str] = Field(..., description="List of embedding vectors (as comma-separated floats)")

class CompareRequest(BaseModel):
    structure1: str = Field(..., description="First RNA secondary structure in dot-bracket notation")
    structure2: Union[str, List[str]] = Field(..., description="Second RNA structure(s) in dot-bracket notation")
    metric: str = Field("squared", description="Distance metric: 'squared' or 'cosine'")

class CompareResponse(BaseModel):
    similarity_score: Union[float, List[float]] = Field(..., description="Similarity score(s) between embeddings")

# Updated Pydantic model to match the actual database columns
class EmbeddingOut(BaseModel):
    id: int
    gene_id: str
    gene_name: Union[str, None] = None
    transcript_id: Union[str, None] = None
    exon_id: Union[str, None] = None
    exon_number: Union[int, None] = None
    chr: Union[str, None] = None
    start: Union[int, None] = None
    end: Union[int, None] = None
    strand: Union[str, None] = None
    rna_sequence: Union[str, None] = None
    rna_ss: str
    seq_len: Union[int, None] = None
    paired_ratio: Union[float, None] = None
    window_start: Union[str, None] = None
    embedding_vector: str

    class Config:
        from_attributes = True

class SearchResult(BaseModel):
    embedding: EmbeddingOut
    metric: float

    class Config:
        from_attributes = True

class SearchRequest(BaseModel):
    structure: str = Field(..., description="RNA secondary structure in dot-bracket notation")
    metric: str = Field("squared", description="Distance metric: 'squared' or 'cosine'")

class SearchResponse(BaseModel):
    results: list[SearchResult] = Field(..., description="Top 30 similar RNA embeddings and their distance metrics")

# Add new Pydantic models for batch embedding endpoint
class BatchStructureItem(BaseModel):
    id: str = Field(..., description="Unique identifier for the structure")
    structure: str = Field(..., description="RNA secondary structure in dot-bracket notation")

class BatchEmbedRequest(BaseModel):
    items: List[BatchStructureItem] = Field(..., description="List of structures with unique ids")

class BatchEmbedResponse(BaseModel):
    embeddings: List[dict] = Field(
        ..., description="List of {id: string, embedding: string} pairs"
    )

# Endpoint to generate embedding(s) for a given RNA structure
@app.post("/embed", response_model=EmbedResponse)
def embed_endpoint(request: EmbedRequest):
    try:
        validate_structure(request.structure)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    try:
        # Pass a list even for a single structure
        emb_lists = get_gin_embedding(model, graph_encoding, [request.structure], device, batch_size=1, cpus=1)
        embeddings = [emb for _, emb in emb_lists[0]]
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
        emb_list1 = get_gin_embedding(model, graph_encoding, [request.structure1], device, batch_size=1, cpus=1)[0]
        vec1 = [float(x) for x in emb_list1[0][1].split(',')]
        
        def compute_similarity(vec_a, vec_b, metric):
            embeddings = [vec_a, vec_b]
            distances = calculate_distances(embeddings, metric=metric, num_workers=1, batch_size=1)
            return distances[0][2]
        
        if isinstance(request.structure2, list):
            scores = []
            emb_lists2 = get_gin_embedding(model, graph_encoding, request.structure2, device, batch_size=1, cpus=1)
            for emb_list2 in emb_lists2:
                vec2 = [float(x) for x in emb_list2[0][1].split(',')]
                if len(vec1) != len(vec2):
                    raise HTTPException(status_code=400, detail="Embedding dimensions do not match.")
                scores.append(compute_similarity(vec1, vec2, request.metric))
            return CompareResponse(similarity_score=scores)
        else:
            emb_list2 = get_gin_embedding(model, graph_encoding, [request.structure2], device, batch_size=1, cpus=1)[0]
            vec2 = [float(x) for x in emb_list2[0][1].split(',')]
            if len(vec1) != len(vec2):
                raise HTTPException(status_code=400, detail="Embedding dimensions do not match.")
            score = compute_similarity(vec1, vec2, request.metric)
            return CompareResponse(similarity_score=score)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error computing similarity: {str(e)}")

# Endpoint to search for similar RNA embeddings in the database
@app.post("/search", response_model=SearchResponse)
def search_endpoint(request: SearchRequest, db: Session = Depends(get_db)):
    try:
        validate_structure(request.structure)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    try:
        # Pass list for consistency
        query_emb_list = get_gin_embedding(model, graph_encoding, [request.structure], device, batch_size=1, cpus=1)[0]
        query_vector = [float(x) for x in query_emb_list[0][1].split(',')]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error computing query embedding: {str(e)}")
    
    try:
        embeddings = db.query(Embedding).all()
        candidate_vectors = []
        valid_records = []
        for rec in embeddings:
            candidate_vec = [float(x) for x in rec.embedding_vector.split(',')]
            if len(query_vector) != len(candidate_vec):
                continue
            candidate_vectors.append(candidate_vec)
            valid_records.append(rec)
        
        batch_size = int(os.getenv("BATCH_SIZE", 512))
        distances = calculate_query_distances(query_vector, candidate_vectors, request.metric, batch_size=batch_size)
        scored = list(zip(distances, valid_records))
        scored.sort(key=lambda x: x[0])
        top30 = scored[:30]
        top30_out = [SearchResult(embedding=EmbeddingOut.from_orm(rec), metric=dist) for dist, rec in top30]
        return SearchResponse(results=top30_out)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching database: {str(e)}")

# New endpoint to compute embeddings from a batch of structures
@app.post("/batch_embed", response_model=BatchEmbedResponse)
def batch_embed_endpoint(request: BatchEmbedRequest):
    # Validate all structures
    for item in request.items:
        try:
            validate_structure(item.structure)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid structure for id {item.id}: {str(e)}")
    
    try:
        # Extract structures from the request
        structures = [item.structure for item in request.items]
        # Compute embeddings (using L=None for a single embedding per structure)
        emb_results = get_gin_embedding(model, graph_encoding, structures, device, L=None, batch_size=128, cpus=2)
        # Prepare output: each emb_results element is a list with one tuple (None, embedding_string)
        output = []
        for idx, emb_list in enumerate(emb_results):
            # Pick the first embedding from each result
            embedding_str = emb_list[0][1]
            output.append({"id": request.items[idx].id, "embedding": embedding_str})
        return BatchEmbedResponse(embeddings=output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error computing batch embeddings: {str(e)}")

# New endpoint to process TSV file and add an embedding_vector column.
@app.post("/tsv_embed")
async def tsv_embed_endpoint(file: UploadFile = File(...)):
    try:
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode("utf-8")), sep="\t")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid TSV file.")
    
    if not {"id", "secondary_structure"}.issubset(df.columns):
        raise HTTPException(status_code=400, detail="TSV must contain 'id' and 'secondary_structure' columns.")
    
    # Compute embeddings for each structure (using L=None for a single embedding)
    structures = df["secondary_structure"].tolist()
    emb_results = get_gin_embedding(model, graph_encoding, structures, device, L=None, batch_size=128, cpus=2)
    embeddings = [emb_list[0][1] for emb_list in emb_results]  # pick the first embedding from each result
    
    df["embedding_vector"] = embeddings
    output = io.StringIO()
    df.to_csv(output, sep="\t", index=False)
    return Response(content=output.getvalue(), media_type="text/tab-separated-values")
