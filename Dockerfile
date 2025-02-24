# Use Node.js image for building frontend
FROM node:20-slim AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install --legacy-peer-deps --production

COPY frontend/ ./
RUN npm run build

# Use Python image with uv pre-installed and nginx
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Install backend dependencies and make pytest available
COPY backend/ backend/
COPY pyproject.toml .
RUN uv sync && uv pip install .
ENV PATH="/app/.venv/bin:/root/.local/bin:/root/.uv/venv/bin:${PATH}" 

# Set up frontend
COPY --from=frontend-builder /app/frontend/build /app/static

EXPOSE 80

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "80"] 
