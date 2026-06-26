import uuid
from datetime import datetime, timezone

from django.utils import timezone as django_timezone
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue

from .qdrant_client import client, COLLECTION_NAME
from .embeddings import embed
from .models import EpisodicMemoryLog


def store_episodic_memory(user, summary: str, category: str = "general"):
    memory_id = str(uuid.uuid4())
    vector = embed(summary)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=memory_id,
                vector=vector,
                payload={
                    "user_id": user.id,
                    "summary": summary,
                    "category": category,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }
            )
        ]
    )

    EpisodicMemoryLog.objects.create(
        user=user,
        qdrant_id=memory_id,
        summary=summary,
        category=category,
        session_date=django_timezone.now().date(),
    )

    return memory_id


def retrieve_relevant_memories(user, current_message: str, top_k: int = 6) -> str:
    vector = embed(current_message)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=user.id)
                )
            ]
        ),
        limit=top_k,
        with_payload=True,
    ).points  # .points gives you the list directly

    if not results:
        return ""

    retrieved_ids = [hit.id for hit in results]
    EpisodicMemoryLog.objects.filter(
        qdrant_id__in=retrieved_ids
    ).update(last_referenced_at=django_timezone.now())

    memory_lines = []
    for hit in results:
        payload = hit.payload
        category = payload.get("category", "general")
        summary = payload.get("summary", "")
        created_at = payload.get("created_at", "")[:10]
        memory_lines.append(f"[{category} | {created_at}] {summary}")

    return "\n".join(memory_lines)