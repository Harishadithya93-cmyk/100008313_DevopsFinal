# ---------- Stage 1: builder ----------
# Full Python image with compilers, used only to install dependencies
FROM python:3.12 AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential pkg-config libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# ---------- Stage 2: runtime ----------
# Slim image that only runs the app (no compilers, smaller and safer)
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Only the small runtime library that mysqlclient needs
RUN apt-get update && apt-get install -y --no-install-recommends libmariadb3 \
    && rm -rf /var/lib/apt/lists/*

# Non-root user
RUN groupadd --system app \
    && useradd --system --gid app --create-home --shell /usr/sbin/nologin app

# Copy installed packages from the builder stage
COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
COPY manage.py ./
COPY config ./config
COPY notes ./notes
COPY --chmod=755 entrypoint.sh ./entrypoint.sh

USER app

EXPOSE 3000

ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:3000", "--workers", "3"]