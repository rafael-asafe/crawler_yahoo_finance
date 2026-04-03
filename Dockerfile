# ── build ────────────────────────────────────────────────────────────────────
FROM python:3.14-slim AS build

WORKDIR /app

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project true

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-interaction --no-ansi

# ── run ──────────────────────────────────────────────────────────────────────
FROM python:3.14-slim AS run

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home appuser

WORKDIR /app

COPY --from=build /app/.venv ./.venv
COPY src/ ./src/

RUN chown -R appuser:appuser /app

USER appuser

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "src/main.py"]