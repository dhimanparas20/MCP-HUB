# Use the official Python slim image (Debian-based, glibc)
FROM python:3.13-slim

# Set environment variables
ARG TZ=Asia/Kolkata
ARG COMPOSE_BAKE=true

ENV TZ=${TZ} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    IPYTHONDIR=/app/.ipython \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tzdata \
        curl \
# enable below if using openai_pdf_image_analyzer.py \
#        libgl1 \
#        poppler-utils \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy the uv and uvx binaries from the official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy only dependency files first for better Docker cache utilization
COPY pyproject.toml uv.lock ./

# Install dependencies with BuildKit cache mount for uv cache
RUN --mount=type=cache,target=/root/.cache/uv \
    UV_HTTP_TIMEOUT=90 uv sync --frozen --no-dev --no-install-project

# Adding Aliases
RUN echo 'alias ipython="uv run ipython"' >> /root/.bashrc

# Copy the entire application code into the container
COPY . .

# Install the project itself (deps already cached from above)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable

# Setup ipython startup
#RUN mkdir -p /app/.ipython/profile_default/startup/ && \
#    cp /app/modules/ipython_startup.py /app/.ipython/profile_default/startup/auto_reload.py

# Default port exposure (documentation)
EXPOSE 8005 8000