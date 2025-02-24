#!/bin/bash

# Load environment variables from .env
set -a
source .env
set +a

# Start nginx
nginx

# Start the FastAPI application
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 