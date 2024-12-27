FROM python:3.9-slim
ARG NODE_PORT=8000
ENV NODE_PORT=${NODE_PORT}

# Install OS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gcc python3-dev libffi-dev libpq-dev iputils-ping netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# First install all dependencies from main PyPI
RUN pip install --no-cache-dir \
    "cryptography>=43.0.3" \
    "fastapi>=0.115.5" \
    "uvicorn[standard]>=0.32.0" \
    "python-jose>=3.3.0" \
    "passlib==1.7.4" \
    "bcrypt==3.2.0" \
    "python-multipart>=0.0.17" \
    "asgi-lifespan>=2.1.0" \
    "aiohttp>=3.8.0" \
    "SQLAlchemy>=1.4.0" \
    "asyncpg>=0.25.0" \
    "psycopg2-binary>=2.9.0" \
    "email-validator" \
    "pydantic[email]" \
    "aiofiles"

# Then install sokoweb from test PyPI with extra index URL for dependencies
RUN pip install --no-cache-dir \
    --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    sokoweb==0.1.13

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

EXPOSE ${NODE_PORT}/tcp
EXPOSE ${NODE_PORT}/udp

CMD ["sh", "-c", "uvicorn sokoweb.sokoweb.api:app --host 0.0.0.0 --port ${NODE_PORT}"]