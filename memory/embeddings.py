import requests as http_requests
import os

JINA_API_URL = "https://api.jina.ai/v1/embeddings"
JINA_API_KEY = os.getenv("JINA_API_KEY", "")
# Jina v3 supports dimensions param — we use 384 to match our existing Qdrant collection
EMBEDDING_DIM = 384


def embed(text: str) -> list[float]:
    """Turn a string into a vector using Jina Embeddings API."""
    if not JINA_API_KEY:
        raise RuntimeError("JINA_API_KEY is not set. Cannot generate embeddings.")

    response = http_requests.post(
        JINA_API_URL,
        headers={
            "Authorization": f"Bearer {JINA_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "jina-embeddings-v3",
            "input": [text],
            "dimensions": EMBEDDING_DIM,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["data"][0]["embedding"]