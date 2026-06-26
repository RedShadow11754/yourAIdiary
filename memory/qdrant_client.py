from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.http.exceptions import UnexpectedResponse
import os

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "episodic_memories"
VECTOR_SIZE = 384

client = QdrantClient(url=QDRANT_URL)


def ensure_collection_exists():
    try:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
        print(f"[Qdrant] Created collection: {COLLECTION_NAME}")
    except UnexpectedResponse as e:
        if "already exists" in str(e):
            print(f"[Qdrant] Collection already exists, skipping.")
        else:
            raise