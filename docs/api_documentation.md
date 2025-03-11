# RNA Similarity API Documentation

## Overview
The RNA Similarity API provides endpoints to compute embeddings for RNA secondary structures and to compare the similarity between two or more structures using either squared distance or cosine similarity.

## Endpoints

### POST /embed
- **Description**: Generate embedding(s) for a given RNA secondary structure.
- **Request Body** (JSON):
  - `structure` (string, required): RNA secondary structure in dot-bracket notation.
- **Response** (JSON):
  - `embeddings`: List of embedding strings.

#### Example Usage for /embed
```
curl -X POST "http://localhost:8000/embed" \
     -H "Content-Type: application/json" \
     -d '{
           "structure": "(((((((..(((............)))..((((.......))))..((((...))))..(((((.......))))))))))))."
         }'
```

### POST /compare
- **Description**: Compare the similarity between RNA structures.
- **Request Body** (JSON):
  - `structure1` (string, required): Reference RNA secondary structure.
  - `structure2` (string or list of strings, required): One or more RNA structures.
  - `metric` (string, optional): Distance metric to use ("squared" or "cosine"). Default is "squared".
- **Response** (JSON):
  - `similarity_score`: A single score (float) or a list of scores corresponding to comparisons.

## Example Usage

### Single Structure Comparison
```
curl -X POST "http://localhost:8000/compare" \
     -H "Content-Type: application/json" \
     -d '{
           "structure1": "(((((((..(((............)))..((((.......))))..((((...))))..(((((.......)))))))))))).",
           "structure2": "((.((((....(((..........))).(((((.......))))).((((...))))..(((((.......))))))))).)).",
           "metric": "squared"
         }'
```

### Batch Comparison
```
curl -X POST "http://localhost:8000/compare" \
     -H "Content-Type: application/json" \
     -d '{
           "structure1": "(((((((..(((............)))..((((.......))))..((((...))))..(((((.......)))))))))))).",
           "structure2": [
             "(((.......((..(((.(((.(((((((.(((((.....(((((((.(.((((.((((((((((((.(((.(.(((........))).).)))))))))).....)))..)).)))).))))))))................(((((.(..(.((((......))))).))))))....))))).(((.....))))))))))...)))..)))..))......)))..",
             "........(((((((....)))))))((((((((..((.(((.((.......)).)))))..)))))......(((.((((....)))).))))))((((((.((.(((((.....((((......)))).)))))((((((...((((((..(((((((((.(((((.(((....))))))))(((((((......)))))))..((((...))))((.(((((.......)))))..))...................))..)))))))))))))))))))..........))))))))........",
             "((.((((....(((..........))).(((((.......))))).((((...))))..(((((.......))))))))).))."
           ],
           "metric": "cosine"
         }'
```

## Running the API
Start the FastAPI application (for example, using Uvicorn):
```
uvicorn api.main:app --reload
```

## Notes
- Ensure that your dot-bracket structures conform to the expected format.
- Validate the request payloads when using batch comparisons.
