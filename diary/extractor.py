import json
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.utils import timezone

from chat.models import Message
from memory.models import UserCoreMemory
from .models import DiaryEntry

from langchain_groq import ChatGroq
import os
import dotenv

dotenv.load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')

llm = ChatGroq(
    api_key=groq_api_key,
    model_name="llama-3.1-8b-instant"
)

MIN_USER_WORDS = 50  # Minimum words from user messages to attempt extraction


def get_todays_transcript(user, today: date) -> tuple[str, int]:
    """
    Returns the full chat transcript for today
    and the total word count of user messages only.
    """
    messages = Message.objects.filter(
        user=user,
        day=today
    ).order_by("created_at")

    if not messages.exists():
        return "", 0

    transcript = ""
    user_word_count = 0

    for msg in messages:
        role = "Me" if msg.role == "user" else "Daisy"
        transcript += f"{role}: {msg.content}\n"
        if msg.role == "user":
            user_word_count += len(msg.content.split())

    return transcript, user_word_count


def get_yesterdays_entry(user, today: date) -> DiaryEntry | None:
    yesterday = today - timedelta(days=1)
    return DiaryEntry.objects.filter(user=user, date=yesterday).first()


def get_previous_entry(user, today: date) -> DiaryEntry | None:
    """Gets the most recent diary entry before today, regardless of gap."""
    return DiaryEntry.objects.filter(
        user=user,
        date__lt=today
    ).order_by("-date").first()


def is_first_entry(user) -> bool:
    return not DiaryEntry.objects.filter(user=user).exists()


def _strip_code_fences(raw: str) -> str:
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
    return raw


def extract_diary_entry(user: User, today: date):
    """
    Main extraction function for one user for one day.
    Returns the created DiaryEntry or None if skipped.
    """

    # --- Check: already extracted today ---
    if DiaryEntry.objects.filter(user=user, date=today).exists():
        print(f"[Diary] Entry already exists for {user.username} on {today}, skipping.")
        return None

    # --- Get transcript and check word count ---
    transcript, user_word_count = get_todays_transcript(user, today)

    if not transcript:
        print(f"[Diary] No messages found for {user.username} on {today}, skipping.")
        return None

    if user_word_count < MIN_USER_WORDS:
        print(f"[Diary] Only {user_word_count} words from {user.username} today (min {MIN_USER_WORDS}), skipping.")
        return None

    # --- Get context inputs ---
    core, _ = UserCoreMemory.objects.get_or_create(user=user)
    core_profile = core.to_prompt_string()

    previous_entry = get_previous_entry(user, today)
    previous_content = previous_entry.display_content if previous_entry else None
    previous_thread = previous_entry.narrative_thread if previous_entry else None
    first_entry = is_first_entry(user)

    # --- Build prompt ---
    if first_entry:
        opening_instruction = """
This is the very first diary entry this person has ever written here.
The entry should feel like the opening page of a diary — an introduction to a life,
a person picking up a pen for the first time and deciding to start telling their story.
It should feel like a beginning, like something is starting today.
"""
    else:
        opening_instruction = "This is a regular diary entry. Continue naturally from where things left off."

    previous_context = ""
    if previous_content:
        previous_context = f"""
YESTERDAY'S DIARY ENTRY:
{previous_content}

RUNNING NARRATIVE THREAD (what has been carrying through this person's life lately):
{previous_thread or "Not established yet."}
"""

    prompt = f"""
You are ghostwriting a private diary entry for a real person.

Your job is to write exactly as if this person sat down tonight and wrote in their own journal.
Write in first person. Write as them, not about them.

The standard you must meet is Anne Frank's diary — emotionally honest, intimate, natural,
occasionally rambling, never clinical, never summarized, never structured like a report.
No one reading this should be able to tell it was written by an AI.

Do NOT:
- Summarize the day like a report
- Use bullet points or headers
- Sound like an assistant or therapist
- Be overly poetic or purple in prose
- Mention the AI or the chat interface
- Say things like "today I had a conversation with my AI friend"
- Start with "Dear Diary" unless it feels completely natural for this person
- DO NOT ever mention the AI it is like a cheat code for you not for the entry

DO:
- Write as this specific person, with their personality and voice
- Let emotions breathe and be specific
- Reference real things they mentioned today
- Be honest about contradictions and confusion
- Let the entry end naturally, not with a tidy conclusion

{opening_instruction}

ABOUT THIS PERSON:
{core_profile}

{previous_context}

TODAY'S CONVERSATION (what they actually talked about today):
{transcript}

---

Now respond ONLY with a valid JSON object. No markdown, no code fences, no explanation.

{{
  "content": "the full diary entry here, written as this person",
  "mood": "single word from this list only: happy / sad / angry / anxious / excited / lonely / peaceful / confused / grateful / numb / hopeful / frustrated / melancholic / content / overwhelmed / other",
  "narrative_thread": "one sentence capturing what is emotionally or narratively carrying through this person's life right now, to be used as context for tomorrow's entry"
}}
"""

    response = llm.invoke(prompt)
    print(prompt)
    raw = response.content.strip()
    raw = _strip_code_fences(raw)

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        print(f"[Diary] Failed to parse JSON for {user.username}: {raw[:200]}")
        return None

    content = result.get("content", "").strip()
    mood = result.get("mood", "other").strip().lower()
    narrative_thread = result.get("narrative_thread", "").strip()

    if not content:
        print(f"[Diary] Empty content returned for {user.username}, skipping.")
        return None

    # Validate mood against allowed choices
    valid_moods = [m[0] for m in DiaryEntry.MOOD_CHOICES]
    if mood not in valid_moods:
        mood = "other"

    entry = DiaryEntry.objects.create(
        user=user,
        date=today,
        content=content,
        mood=mood,
        narrative_thread=narrative_thread,
    )

    print(f"[Diary] Entry created for {user.username} | {today} | mood: {mood}")
    return entry