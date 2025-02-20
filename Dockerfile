# Use Node.js image for building frontend
FROM node:20-slim AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install --legacy-peer-deps --production

COPY frontend/ ./
RUN npm run build

# Use Python image with uv pre-installed and nginx
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install nginx
RUN apt-get update && apt-get install -y nginx

WORKDIR /app

# Copy backend code
COPY backend/ backend/
COPY pyproject.toml .

# Install backend dependencies and make pytest available
RUN uv sync && uv pip install .
ENV PATH="/root/.local/bin:/root/.uv/venv/bin:${PATH}"

# Copy frontend build and nginx config
COPY --from=frontend-builder /app/frontend/build /usr/share/nginx/html
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Expose ports
EXPOSE 80 8000

# Create startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"] 