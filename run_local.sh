#!/bin/bash

# Stop and remove any existing container with the same name
echo "Stopping any existing simplify container..."
docker stop simplify 2>/dev/null || true
docker rm simplify 2>/dev/null || true

# Build the Docker image
echo "Building Docker image..."
docker build -t simplify .

# Run the container
echo "Starting container..."
docker run -d \
    --env-file .env \
    --name simplify \
    -p 80:80 \
    -p 7860:7860 \
    simplify

echo "Services started!"
echo "Frontend available at: http://localhost:7860"
echo "Backend available at: http://localhost:7860"
echo ""
echo "To view logs: docker logs -f simplify"
echo "To stop: docker stop simplify" 