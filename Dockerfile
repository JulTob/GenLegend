# Gen Legend, the Player Character generator, as one container.
#   docker build --build-arg BUILD_SHA=$(git rev-parse --short HEAD) -t gen-legends .
#   docker run -p 8080:8080 gen-legends
#   gcloud run deploy gen-legends --source . --region us-central1 --allow-unauthenticated
#
# The Cloud Run service is gen-legends, with an s, and genlegend.eu maps to
# it. Deploying to gen-legend builds and succeeds and changes nothing the
# domain serves, because it creates a second service instead.
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# TagKit installs from a git URL.
RUN apt-get update \
 && apt-get install -y --no-install-recommends git \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ARG BUILD_SHA=unknown
ENV BUILD_SHA=${BUILD_SHA} \
    PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "shiny run --host 0.0.0.0 --port ${PORT} app.main:app"]
