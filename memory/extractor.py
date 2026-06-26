import json
from langchain_groq import ChatGroq
from django.conf import settings
from chat.models import Message
from .models import UserCoreMemory, ChatSession
from .episodic import store_episodic_memory
import os
import dotenv

dotenv.load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')

llm = ChatGroq(
    api_key=groq_api_key,
    model_name="llama-3.1-8b-instant"
)


def _get_session_messages(session: ChatSession) -> str:
    """Pull all messages from this session as a readable transcript."""
    messages = Message.objects.filter(
        user=session.user,
        created_at__gte=session.started_at,
        created_at__lte=session.last_activity_at
    ).order_by("created_at")

    transcript = ""
    for msg in messages:
        role = "User" if msg.role == "user" else "AI"
        transcript += f"{role}: {msg.content}\n"
    return transcript


def extract_episodic_memories(session: ChatSession):
    """
    Ask the LLM to extract meaningful episodic memories from the session.
    Stores each one in Qdrant.
    """
    transcript = _get_session_messages(session)
    if not transcript.strip():
        return

    prompt = f"""
You are a memory extraction system for a personal AI friend.

Read the following conversation and extract any moments, events, emotions, or revelations 
that are worth remembering long-term about this person.

Only extract things that are genuinely meaningful — personal events, emotional moments, 
things they shared about their life, relationships, struggles, or wins.
Do NOT extract small talk or generic exchanges.

For each memory, assign a category from: emotion, relationship, work, health, family, personal_growth, life_event, other

Respond ONLY with a valid JSON array. No explanation, no preamble. Example format:
[
  {{"summary": "User mentioned feeling overwhelmed by their job and considering quitting.", "category": "work"}},
  {{"summary": "User's best friend Joe got married last weekend. User felt bittersweet about it.", "category": "relationship"}}
]

If there is nothing worth remembering, respond with an empty array: []

CONVERSATION:
{transcript}
"""

    response = llm.invoke(prompt)
    raw = response.content.strip()

    # Strip markdown code fences
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        memories = json.loads(raw)
    except json.JSONDecodeError:
        print(f"[Extractor] Failed to parse episodic memories JSON: {raw}")
        return


    for memory in memories:
        summary = memory.get("summary", "").strip()
        category = memory.get("category", "general").strip()
        if summary:
            store_episodic_memory(session.user, summary, category)

    print(f"[Extractor] Stored {len(memories)} episodic memories for user {session.user.username}")


def update_core_memory(session: ChatSession):
    transcript = _get_session_messages(session)
    if not transcript.strip():
        return

    core, _ = UserCoreMemory.objects.get_or_create(user=session.user)
    existing_profile = core.to_prompt_string()

    prompt = f"""
You are a core memory updater for a personal AI friend system.

Your job is to update what is permanently known about this user based on their latest conversation.
You have their existing profile and a new conversation. Update only what has changed or is newly learned.

Existing profile:
{existing_profile}

New conversation:
{transcript}

Respond ONLY with a valid JSON object. No explanation, no preamble, no markdown, no code fences.
Only include fields that have new or updated information. Leave out fields with no updates.

Available fields:
- known_name (string)
- age (string)
- occupation (string)  
- location (string)
- relationships (string — describe key people in their life)
- personality_observations (string — behavioral patterns you've noticed)
- recurring_themes (string — topics that come up repeatedly)
- important_life_events (string — significant events)
- current_life_context (string — what's going on in their life right now)

Example response:
{{"current_life_context": "Recently started a new job.", "known_name": "Daniel"}}
"""

    response = llm.invoke(prompt)
    raw = response.content.strip()

    # Strip markdown code fences if LLM wraps response in them
    if raw.startswith("```"):
        raw = raw.split("```")[1]          # get content between first pair of fences
        if raw.startswith("json"):
            raw = raw[4:]                  # strip the "json" language tag
        raw = raw.strip()

    try:
        updates = json.loads(raw)
    except json.JSONDecodeError:
        print(f"[Extractor] Failed to parse core memory JSON: {raw}")
        return

    for field, value in updates.items():
        if hasattr(core, field) and value:
            setattr(core, field, value)
    core.save()

    print(f"[Extractor] Updated core memory for user {session.user.username}")

def process_session(session: ChatSession):
    """Main entry point. Runs both extractors then marks session as processed."""
    extract_episodic_memories(session)
    update_core_memory(session)

    session.memory_extracted = True
    session.ended_at = session.last_activity_at
    session.save(update_fields=["memory_extracted", "ended_at"])