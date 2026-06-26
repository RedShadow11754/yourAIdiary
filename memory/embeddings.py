from sentence_transformers import SentenceTransformer

# Loaded once at startup — not on every request
_model = None

def get_embedding_model():
    global _model
    if _model is None:
        print("[Embeddings] Loading sentence-transformer model...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        print("[Embeddings] Model loaded.")
    return _model


def embed(text: str) -> list[float]:
    """Turn a string into a vector."""
    model = get_embedding_model()
    return model.encode(text, normalize_embeddings=True).tolist()