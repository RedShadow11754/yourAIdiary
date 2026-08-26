from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import os

QDRANT_URL = os.getenv("QDRANT_URL", "")
COLLECTION_NAME = "episodic_memories"
VECTOR_SIZE = 384

# Only create client if URL is set — avoids crash during startup on Render
client = QdrantClient(url=QDRANT_URL) if QDRANT_URL else None


def ensure_collection_exists():
    """Create the Qdrant collection if it doesn't exist.
    Gracefully skips if Qdrant is unreachable (e.g. during build on Render).
    """
    if not client:
        print("[Qdrant] QDRANT_URL not set, skipping collection setup.")
        return
    try:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
        print(f"[Qdrant] Created collection: {COLLECTION_NAME}")
    except Exception as e:
        if "already exists" in str(e):
            print(f"[Qdrant] Collection already exists, skipping.")
        else:
            print(f"[Qdrant] Warning: could not verify collection: {e}")