FROM python:3.11.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

WORKDIR /app

COPY requirements.txt runtime.txt ./

RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt \
    && python -m pip install "uvicorn[standard]" python-multipart

COPY main.py ./
COPY agents ./agents
COPY background ./background
COPY config ./config
COPY db ./db
COPY flows ./flows
COPY graph ./graph
COPY helper ./helper
COPY mcp_setup ./mcp_setup
COPY middleware ./middleware
COPY models ./models
COPY prompts ./prompts
COPY router ./router
COPY telemetry ./telemetry
COPY tools ./tools

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
