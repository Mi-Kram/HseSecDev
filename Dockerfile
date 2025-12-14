# Build stage
FROM python:3.11-slim AS build
WORKDIR /app
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt
COPY . .

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
RUN useradd -m appuser
COPY --from=build /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=build /usr/local/bin /usr/local/bin
COPY . .
EXPOSE 8000
HEALTHCHECK CMD curl -f http://localhost:8000/api/health || exit 1
USER appuser
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
