FROM python:3.13-slim

# 1. Install system dependencies (curl/git are often needed for python packages)
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# 2. Install uv (using the official copier is faster/cleaner than pip)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 3. Set working directory
WORKDIR /code

# 4. Copy ONLY dependency files first (for Docker caching)
COPY pyproject.toml ./

# 5. Install dependencies
# --system: Installs into the container's main Python environment (fixes your error)
# -r pyproject.toml: Reads the dependencies directly from your file
RUN uv pip install --system -r pyproject.toml

# 6. Copy the rest of your application code
COPY . .

# 7. Expose the port
EXPOSE 8000

