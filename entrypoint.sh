#!/bin/bash
# Source conda’s bash functions so we can use "conda activate"
source /opt/conda/etc/profile.d/conda.sh
conda activate gin_api_env
# Execute uvicorn with unbuffered output
exec uvicorn api.main:app --host 0.0.0.0 --port 8000 --log-level info

