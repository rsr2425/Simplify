# Use Node.js image for building frontend
FROM node:20-slim AS frontend-builder

WORKDIR /app/frontend

# Copy package files first for better caching
COPY frontend/package*.json ./
RUN npm cache clean --force && \
    npm install --legacy-peer-deps --force

# Copy only the necessary frontend files
COPY frontend/public ./public
COPY frontend/src ./src
COPY frontend/tsconfig.json .
COPY frontend/jest.config.js .
COPY frontend/.env .

# Show more verbose output during build
RUN npm run build --verbose

# Use Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Copy backend code
COPY backend/ backend/
COPY pyproject.toml .

# Install backend dependencies and make pytest available
RUN uv sync && uv pip install .
ENV PATH="/root/.local/bin:/root/.uv/venv/bin:${PATH}"

# Copy frontend build
COPY --from=frontend-builder /app/frontend/build /app/frontend/build

# Add uv's bin directory to PATH
ENV PATH="/app/.venv/bin:/root/.local/bin:/root/.uv/venv/bin:${PATH}"

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"] 