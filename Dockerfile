# Use Node.js image for building frontend
FROM node:20-slim AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install --legacy-peer-deps --production

COPY frontend/ ./
RUN npm run build

# Use Python image with uv pre-installed and nginx
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update && apt-get install -y nginx

WORKDIR /app


# Install backend dependencies and make pytest available
COPY backend/ backend/
COPY pyproject.toml .
RUN uv sync && uv pip install .
ENV PATH="/root/.local/bin:/root/.uv/venv/bin:${PATH}"

# Set up frontend
COPY --from=frontend-builder /app/frontend/build /usr/share/nginx/html
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Add uv's bin directory to PATH
ENV PATH="/app/.venv/bin:/root/.local/bin:/root/.uv/venv/bin:${PATH}" 

EXPOSE 80 8000

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
