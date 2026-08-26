from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PayloadSchemaType
import os

QDRANT_URL = os.getenv("QDRANT_URL", "")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
COLLECTION_NAME = "episodic_memories"
VECTOR_SIZE = 384

# Only create client if URL is set — avoids crash during startup on Render
if QDRANT_URL:
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY if QDRANT_API_KEY else None)
else:
    client = None


def ensure_collection_exists():
    """Create the Qdrant collection and payload index if they don't exist.
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
            print(f"[Qdrant] Warning: could not create collection: {e}")

    # Create payload index on user_id for efficient filtering
    try:
        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="user_id",
            field_schema=PayloadSchemaType.INTEGER,
        )
        print(f"[Qdrant] Payload index on user_id ready.")
    except Exception as e:
        if "already exists" in str(e) or "Index already exists" in str(e):
            pass  # fine
        else:
            print(f"[Qdrant] Warning: could not create payload index: {e}")