# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Use an ARG for the port so we can set it at build time if desired
ARG NODE_PORT=8000

# Persist it as an environment variable for runtime
ENV NODE_PORT=${NODE_PORT}

# Install system dependencies including curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    python3-dev \
    libffi-dev \
    libpq-dev \
    iputils-ping \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY setup.py ./
COPY src ./src/
COPY create_tables.py ./
COPY wait_for_postgres.py ./

# Install the Python package and dependencies
RUN pip install --no-cache-dir -e .

# Set environment variables
ENV PYTHONPATH=/app/src \
    PYTHONUNBUFFERED=1

# Expose ports for both TCP and UDP communication
EXPOSE ${NODE_PORT}/tcp
EXPOSE ${NODE_PORT}/udp

# Command to run the app
CMD ["sh", "-c", "uvicorn sokoweb.api:app --host 0.0.0.0 --port ${NODE_PORT}"]