# Memory System — Complete Architecture & Pipeline Reference

> **Purpose:** This document explains how the AI friend remembers things about users — from the moment a message is sent, through extraction, storage, and retrieval. Every file, every model, every data flow is covered.

---

## Table of Contents

1. [High-Level Architecture](#1-high-level-architecture)
2. [The Three Memory Types](#2-the-three-memory-types)
3. [File-by-File Breakdown](#3-file-by-file-breakdown)
4. [The Full Pipeline — End to End](#4-the-full-pipeline--end-to-end)
5. [Worked Example: Message Through Pipeline](#5-worked-example-message-through-pipeline)
6. [Infrastructure & Config](#6-infrastructure--config)
7. [Data Flow Diagram](#7-data-flow-diagram)

---

## 1. High-Level Architecture

The memory system has **two operating modes**:

| Mode | When | What Happens |
|------|------|-------------|
| **Real-time Retrieval** | Every chat message | Pull core profile + search episodic memories → inject into AI prompt |
| **Background Extraction** | Every 10 min (Celery Beat) | Process expired sessions → extract episodic memories + update core profile |

There is also a **Diary Pipeline** (midnight daily) that uses core memory for context but is separate from the memory system itself.

**Tech Stack for Memory:**

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Core Memory Store | Django ORM (SQLite) | Structured user profile |
| Episodic Memory Store | Qdrant (vector DB) | Semantic search over past memories |
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`) | 384-dim vectors for similarity search |
| LLM (Extraction) | Groq + `llama-3.1-8b-instant` | Extract memories from transcripts |
| Task Queue | Celery + Redis | Background processing |
| Session Tracking | Django ORM (SQLite) | Track active chat sessions |

---

## 2. The Three Memory Types

### 2a. Core Memory (`UserCoreMemory`)

**What it is:** A permanent, always-injected profile of the user. Think of it as the AI's "knowledge base" about who this person is. It is **updated (not appended)** after each session.

**Model fields** (`memory/models.py` → `UserCoreMemory`):

```python
class UserCoreMemory(models.Model):
    user = OneToOneField(User)              # One profile per user

    # Structured fast-access fields
    known_name = CharField(max_length=100)      # "Daniel"
    age = CharField(max_length=20)              # "28"
    occupation = CharField(max_length=100)      # "Software engineer"
    location = CharField(max_length=100)        # "Portland, OR"

    # Freeform evolving fields — AI writes and rewrites these
    relationships = TextField()        # "Sister: Maya, close but complicated. Best friend: Joe."
    personality_observations = TextField()  # "Tends to overthink. Humor is dry."
    recurring_themes = TextField()     # "Work stress, family tension, self-doubt."
    important_life_events = TextField()     # "Lost job in March. Started therapy in April."
    current_life_context = TextField()     # "Currently going through a breakup."
```

**How it's used:** The `to_prompt_string()` method formats it into a clean text block that gets injected into every AI chat prompt under the section `"WHAT I KNOW ABOUT YOU"`.

**Example `to_prompt_string()` output:**
```
Name: Daniel
Age: 28
Occupation: Software engineer
Location: Portland, OR
Key relationships: Sister: Maya, close but complicated. Best friend: Joe.
Personality: Tends to overthink. Humor is dry. Sometimes deflects with jokes when things get serious.
Recurring themes in their life: Work stress, family tension, self-doubt.
Important life events: Lost job in March 2025. Started therapy in April.
Current life context: Going through a breakup with Alex. Started dating again but feels conflicted.
```

**How it gets updated:** The LLM in `memory/extractor.py` → `update_core_memory()` compares the existing profile with a new conversation transcript and outputs only the fields that changed. It's a **merge, not overwrite** — only fields present in the LLM's JSON response get updated.

---

### 2b. Episodic Memory (Qdrant + `EpisodicMemoryLog`)

**What it is:** Individual meaningful moments, events, or revelations from conversations. Stored as **vectors** in Qdrant for semantic similarity search. When the user sends a new message, the system finds the most relevant past memories.

**Storage layer** (`memory/episodic.py` → `store_episodic_memory()`):

Each episodic memory has:
- **vector** — 384-dim embedding of the summary text (via `all-MiniLM-L6-v2`)
- **payload** — JSON with `user_id`, `summary`, `category`, `created_at`
- **UUID** — unique ID stored in both Qdrant and Django

**Categories:** `emotion`, `relationship`, `work`, `health`, `family`, `personal_growth`, `life_event`, `other`

**Django mirror** (`memory/models.py` → `EpisodicMemoryLog`):

```python
class EpisodicMemoryLog(models.Model):
    user = ForeignKey(User)
    qdrant_id = CharField(unique=True)    # UUID that matches Qdrant
    summary = TextField()                  # "User mentioned feeling overwhelmed by job"
    category = CharField()                 # "work"
    session_date = DateField()
    last_referenced_at = DateTimeField()   # Updated when retrieved during chat
    is_archived = BooleanField()           # For admin management
```

This is a **local mirror** so you can manage, archive, and reference memories without hitting Qdrant for admin operations.

---

### 2c. LongMemory (Minimal/Unused)

```python
class LongMemory(models.Model):
    user = ForeignKey(User)
    message = TextField()
```

This model exists in `memory/models.py` but is **not actively used** in any pipeline. It appears to be a stub or placeholder for a future "long-term fact storage" system that hasn't been implemented yet.

---

## 3. File-by-File Breakdown

### `memory/models.py` — Data Models

| Model | Purpose |
|-------|---------|
| `LongMemory` | Unused placeholder |
| `UserCoreMemory` | Permanent user profile (OneToOne with User) |
| `EpisodicMemoryLog` | Django mirror of Qdrant memories |
| `ChatSession` | Tracks chat sessions for extraction triggering |

**Key `ChatSession` fields:**
```python
class ChatSession(models.Model):
    user = ForeignKey(User)
    started_at = DateTimeField(auto_now_add=True)
    last_activity_at = DateTimeField()      # Updated on every message
    ended_at = DateTimeField(null=True)     # Set when session closes
    memory_extracted = BooleanField(default=False)  # Has extraction run?
```

Sessions close after **90 minutes of inactivity**.

---

### `memory/session_tracker.py` — Session Lifecycle

```python
SESSION_TIMEOUT_MINUTES = 90
```

**`get_or_create_session(user)`** — Called on every incoming chat message:
1. Look for an active session (no `ended_at`, `last_activity_at` within 90 min)
2. If found → update `last_activity_at` to now, return it
3. If not found → close any lingering open sessions, create a new one

**`get_expired_unprocessed_sessions()`** — Used by Celery task:
- Finds sessions where `ended_at IS NULL`, `memory_extracted=False`, and `last_activity_at` is older than 90 minutes
- These are the sessions that need memory extraction

---

### `memory/qdrant_client.py` — Vector DB Setup

```python
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "episodic_memories"
VECTOR_SIZE = 384    # Matches all-MiniLM-L6-v2 output
```

- Creates a Qdrant client connected to localhost:6333
- `ensure_collection_exists()` creates the collection with **cosine distance** if it doesn't exist
- The collection stores vectors with payloads (user_id, summary, category, created_at)

---

### `memory/embeddings.py` — Text → Vector

```python
_model = None  # Loaded once at startup

def get_embedding_model():
    # Lazy-loads sentence-transformers model
    # Model: all-MiniLM-L6-v2 (384 dimensions)
    # Loaded once, reused across all requests

def embed(text: str) -> list[float]:
    # Converts text → 384-dim normalized vector
    # Used for both storing and searching memories
```

**Key detail:** The model is loaded **once at startup** (lazy singleton), not on every request. This keeps embedding fast.

---

### `memory/episodic.py` — Store & Retrieve Episodic Memories

**`store_episodic_memory(user, summary, category)`:**
1. Generate a UUID for the memory
2. Embed the summary text → 384-dim vector
3. Upsert to Qdrant: `{id, vector, payload: {user_id, summary, category, created_at}}`
4. Create `EpisodicMemoryLog` in Django (mirror record)
5. Return the UUID

**`retrieve_relevant_memories(user, current_message, top_k=6)`:**
1. Embed the current message → 384-dim vector
2. Query Qdrant: find top 6 most similar memories **for this user only** (filtered by `user_id`)
3. Update `last_referenced_at` on the retrieved `EpisodicMemoryLog` records
4. Format results as: `[category | date] summary` (one per line)
5. Return the formatted string

**Example retrieval output:**
```
[work | 2025-06-15] User mentioned feeling overwhelmed by their job and considering quitting.
[relationship | 2025-06-18] User's best friend Joe got married last weekend. User felt bittersweet about it.
[personal_growth | 2025-06-20] User started going to therapy and feels it's helping with anxiety.
```

---

### `memory/extractor.py` — LLM-Based Memory Extraction

This is the **brain** of the extraction pipeline. It uses Groq + `llama-3.1-8b-instant` for two tasks:

**Task 1: `extract_episodic_memories(session)`**
1. Pull all messages from the session as a transcript
2. Ask LLM: "Extract meaningful moments from this conversation"
3. LLM returns JSON array: `[{"summary": "...", "category": "..."}]`
4. For each memory → `store_episodic_memory()`

**LLM Prompt (simplified):**
```
You are a memory extraction system for a personal AI friend.
Read the conversation and extract moments worth remembering long-term.
Only extract genuinely meaningful things — personal events, emotional moments, struggles, wins.
Do NOT extract small talk.
For each memory, assign a category.
Respond ONLY with a valid JSON array.
```

**Task 2: `update_core_memory(session)`**
1. Pull session transcript
2. Get existing `UserCoreMemory` profile
3. Ask LLM: "Update this profile based on the new conversation"
4. LLM returns JSON object with only changed fields
5. Merge updates into `UserCoreMemory`

**LLM Prompt (simplified):**
```
You are a core memory updater for a personal AI friend system.
Update what is permanently known about this user based on the latest conversation.
You have their existing profile and a new conversation.
Update only what has changed or is newly learned.
Respond ONLY with a valid JSON object with only updated fields.
```

**`process_session(session)`** — Main entry point:
1. `extract_episodic_memories(session)`
2. `update_core_memory(session)`
3. Mark session as `memory_extracted=True` and set `ended_at`

---

### `memory/tasks.py` — Celery Background Task

```python
@shared_task
def run_memory_extraction():
    # Runs every 10 minutes (configured in config/settings.py)
    # Finds expired unprocessed sessions
    # For each: calls process_session()
```

---

### `memory/logic.py` — Daily Chat Context

```python
def get_today_chats(user):
    # Returns today's messages as a formatted string (max 40 messages)
    # Used to give the AI "recent conversation context"
    # Output format: "User: ...\nAI: ...\n"
```

This is **not** memory extraction — it's just pulling today's messages for the chat prompt's `RECENT CHAT CONTEXT` section.

---

### `chat/views.py` — Where Memory Meets Chat

The `ChatView.post()` method is where everything comes together:

```python
def post(self, request):
    message = request.data.get('message')

    # 1. Track session
    get_or_create_session(request.user)

    # 2. Pull core profile (always injected)
    core, _ = UserCoreMemory.objects.get_or_create(request.user)
    core_memory_str = core.to_prompt_string()

    # 3. Retrieve relevant episodic memories (semantic search)
    episodic_memories_str = retrieve_relevant_memories(request.user, message)

    # 4. Build combined context
    ultimate_info = ""
    if core_memory_str:
        ultimate_info += f"WHAT I KNOW ABOUT YOU:\n{core_memory_str}\n\n"
    if episodic_memories_str:
        ultimate_info += f"RELEVANT MEMORIES FROM OUR PAST CONVERSATIONS:\n{episodic_memories_str}"

    # 5. Get today's chat context
    daily_context, _ = get_today_chats(user=request.user)

    # 6. Build personality settings
    user_settings = UserPersonality.objects.get(user=request.user)

    # 7. Call AI with all context
    reply = chat_service.answer(
        message,
        daily_chats=daily_context,
        user_name=user_settings.user_name,
        ...,  # personality settings
        ultimate_info=ultimate_info,  # ← THIS IS THE MEMORY INJECTION
    )

    # 8. Save both messages
    Message.objects.create(user=request.user, role="user", content=message)
    Message.objects.create(user=request.user, role="ai", content=reply)
```

**The `ultimate_info` variable** is the key — it combines:
- Core memory (always present, structured profile)
- Episodic memories (relevant to current message, semantically retrieved)

Both are injected into the LLM prompt under the `"ULTIMATE USER INFO"` section.

---

### `config/settings.py` — Celery Beat Schedule

```python
CELERY_BEAT_SCHEDULE = {
    # Memory extraction — every 10 minutes
    "run-memory-extraction-every-10-minutes": {
        "task": "memory.tasks.run_memory_extraction",
        "schedule": 600,  # 10 minutes
    },
    # Diary extraction — every day at midnight
    "run-diary-extraction-at-midnight": {
        "task": "diary.tasks.run_diary_extraction",
        "schedule": crontab(hour=0, minute=0),
    },
}
```

---

## 4. The Full Pipeline — End to End

### Phase A: Real-Time Retrieval (Every Chat Message)

```
User sends: "I'm thinking about quitting my job"
    │
    ▼
ChatView.post()
    │
    ├──→ get_or_create_session(user)
    │       ├── Active session exists? → update last_activity_at
    │       └── No active session? → close old, create new ChatSession
    │
    ├──→ UserCoreMemory.to_prompt_string()
    │       Returns: "Name: Daniel\nAge: 28\nOccupation: Software engineer\n..."
    │
    ├──→ retrieve_relevant_memories(user, "I'm thinking about quitting my job")
    │       ├── embed("I'm thinking about quitting my job") → 384-dim vector
    │       ├── Qdrant query: top 6 similar memories for this user
    │       ├── Updates last_referenced_at on retrieved logs
    │       └── Returns: "[work | 2025-06-15] User mentioned feeling overwhelmed by job..."
    │
    ├──→ get_today_chats(user)
    │       Returns: "User: ...\nAI: ...\n" (max 40 messages today)
    │
    ├──→ Build ultimate_info
    │       "WHAT I KNOW ABOUT YOU:\nName: Daniel\n...\n\n
    │        RELEVANT MEMORIES FROM OUR PAST CONVERSATIONS:\n[work | ...] ..."
    │
    ├──→ chat_service.answer()  ← LLM generates response with all context
    │
    └──→ Save user message + AI reply to Message table
```

### Phase B: Background Extraction (Every 10 Minutes)

```
Celery Beat fires run_memory_extraction()
    │
    ▼
get_expired_unprocessed_sessions()
    │   Finds: ChatSessions where
    │   - ended_at IS NULL (still "open")
    │   - memory_extracted = False
    │   - last_activity_at < 90 minutes ago
    │
    ▼
For each session:
    │
    ├──→ process_session(session)
    │       │
    │       ├──→ extract_episodic_memories(session)
    │       │       │
    │       │       ├──→ _get_session_messages(session)
    │       │       │       Pulls all Message objects in the session time range
    │       │       │       Formats as: "User: ...\nAI: ...\n"
    │       │       │
    │       │       ├──→ LLM Prompt: "Extract meaningful memories from this conversation"
    │       │       │       Returns: [{"summary": "...", "category": "..."}, ...]
    │       │       │
    │       │       └──→ For each memory:
    │       │               store_episodic_memory(user, summary, category)
    │       │                   ├── embed(summary) → vector
    │       │                   ├── Qdrant upsert: {id, vector, payload}
    │       │                   └── EpisodicMemoryLog.objects.create(...)
    │       │
    │       ├──→ update_core_memory(session)
    │       │       │
    │       │       ├──→ _get_session_messages(session) → transcript
    │       │       ├──→ UserCoreMemory.to_prompt_string() → existing profile
    │       │       │
    │       │       ├──→ LLM Prompt: "Update this profile based on new conversation"
    │       │       │       Returns: {"current_life_context": "...", "occupation": "..."}
    │       │       │
    │       │       └──→ core.save()  ← merges only changed fields
    │       │
    │       └──→ session.memory_extracted = True
    │            session.ended_at = session.last_activity_at
    │            session.save()
    │
    └──→ (next session...)
```

---

## 5. Worked Example: Message Through Pipeline

### Setup: User "Daniel" has been chatting for a few days

**Existing Core Memory:**
```
Name: Daniel
Age: 28
Occupation: Software engineer
Location: Portland, OR
Key relationships: Best friend Joe.
Personality: Tends to overthink. Humor is dry.
Recurring themes in their life: Work stress.
Important life events: None recorded yet.
Current life context: None recorded yet.
```

**Existing Episodic Memories in Qdrant:**
| ID | Summary | Category | Date |
|----|---------|----------|------|
| abc-123 | User mentioned feeling overwhelmed by their job and considering quitting. | work | 2025-06-15 |
| def-456 | User's best friend Joe got married last weekend. User felt bittersweet. | relationship | 2025-06-18 |

---

### Step 1: Daniel sends a message

**Input:** `"I told my boss today that I'm putting in my two weeks. I'm terrified but also relieved."`

### Step 2: Real-time processing (ChatView.post)

**2a. Session tracking:**
```python
get_or_create_session(daniel)
# → Creates new ChatSession (or reuses active one)
# → ChatSession { user: daniel, started_at: now, last_activity_at: now }
```

**2b. Core memory retrieval:**
```python
core.to_prompt_string()
# → "Name: Daniel\nAge: 28\nOccupation: Software engineer\n..."
```

**2c. Episodic memory retrieval:**
```python
retrieve_relevant_memories(daniel, "I told my boss today that I'm putting in my two weeks...")
```
- Embeds the message → vector
- Queries Qdrant: finds `abc-123` (high similarity — both about job/quitting)
- Also finds `def-456` (medium similarity — emotional content about Joe's wedding)
- Returns:
```
[work | 2025-06-15] User mentioned feeling overwhelmed by their job and considering quitting.
[relationship | 2025-06-18] User's best friend Joe got married last weekend. User felt bittersweet about it.
```

**2d. Combined into `ultimate_info`:**
```
WHAT I KNOW ABOUT YOU:
Name: Daniel
Age: 28
Occupation: Software engineer
Location: Portland, OR
Key relationships: Best friend Joe.
Personality: Tends to overthink. Humor is dry.
Recurring themes in their life: Work stress.

RELEVANT MEMORIES FROM OUR PAST CONVERSATIONS:
[work | 2025-06-15] User mentioned feeling overwhelmed by their job and considering quitting.
[relationship | 2025-06-18] User's best friend Joe got married last weekend. User felt bittersweet about it.
```

**2e. AI generates response** (with all context — personality, daily chats, ultimate_info):
> "Dude. That's huge. I remember you were stressed about this for weeks — honestly I'm proud of you for actually pulling the trigger. How'd your boss take it?"

**2f. Messages saved:**
```python
Message(user=daniel, role="user", content="I told my boss today...")
Message(user=daniel, role="ai", content="Dude. That's huge...")
```

---

### Step 3: 90 minutes pass — Session expires

Daniel stops chatting. After 90 minutes, the session is "expired" — no new messages.

### Step 4: Celery Beat fires (every 10 minutes)

```python
run_memory_extraction()
# → Finds Daniel's session: last_activity_at is 90+ min ago, memory_extracted=False
```

### Step 5: `process_session(session)` runs

**5a. Extract episodic memories:**

Transcript pulled:
```
User: I told my boss today that I'm putting in my two weeks. I'm terrified but also relieved.
AI: Dude. That's huge. I remember you were stressed about this for weeks — honestly I'm proud of you...
```

LLM is prompted → returns:
```json
[
  {
    "summary": "User quit their job today by giving two weeks notice. They feel both terrified and relieved after weeks of deliberation.",
    "category": "work"
  },
  {
    "summary": "User shared a major life decision with the AI and expressed vulnerability about fear and relief.",
    "category": "personal_growth"
  }
]
```

Each gets stored:
- `store_episodic_memory(daniel, "User quit their job today...", "work")` → new Qdrant point + EpisodicMemoryLog
- `store_episodic_memory(daniel, "User shared a major life decision...", "personal_growth")` → new Qdrant point + EpisodicMemoryLog

**5b. Update core memory:**

Existing profile: `"Name: Daniel\nAge: 28\nOccupation: Software engineer\n..."`

LLM is prompted → returns:
```json
{
  "recurring_themes": "Work stress, career transitions, self-doubt about big decisions.",
  "important_life_events": "Quit software engineering job in late June 2025.",
  "current_life_context": "Just quit their job. Going through a major career transition. Feels terrified but relieved."
}
```

Only these 3 fields are updated on `UserCoreMemory`. Everything else stays the same.

**5c. Session marked complete:**
```python
session.memory_extracted = True
session.ended_at = session.last_activity_at  # ≈ 90 min ago
session.save()
```

---

### Step 6: Next time Daniel chats

Now when Daniel sends a message like `"How's your day going?"`, the system:

1. **Core memory** now includes: `"Important life events: Quit software engineering job in late June 2025."` and `"Current life context: Just quit their job..."` → AI knows about the job quit
2. **Episodic memories** now include the two new memories about quitting → semantic search can surface them
3. The AI can say things like `"Hey, it's only been a few days since you quit — how are you adjusting to the freedom?"`

---

## 6. Infrastructure & Config

### Qdrant (Vector Database)

| Setting | Value |
|---------|-------|
| URL | `http://localhost:6333` (env: `QDRANT_URL`) |
| Collection | `episodic_memories` |
| Vector size | 384 dimensions |
| Distance | Cosine similarity |
| Payload fields | `user_id`, `summary`, `category`, `created_at` |

### Embeddings

| Setting | Value |
|---------|-------|
| Model | `all-MiniLM-L6-v2` (via `sentence-transformers`) |
| Dimensions | 384 |
| Normalization | Yes (`normalize_embeddings=True`) |
| Loading | Lazy singleton (loaded once at first use) |

### LLM (Extraction)

| Setting | Value |
|---------|-------|
| Provider | Groq |
| Model | `llama-3.1-8b-instant` |
| Used for | Episodic extraction + Core memory updates |
| Input | Session transcripts |
| Output | JSON (array for episodic, object for core) |

### Celery

| Setting | Value |
|---------|-------|
| Broker | Redis (`redis://localhost:6379/0`) |
| Beat: Memory extraction | Every 10 minutes |
| Beat: Diary extraction | Midnight daily (crontab) |
| Worker pool | `solo` (single process) |

### Session Management

| Setting | Value |
|---------|-------|
| Timeout | 90 minutes of inactivity |
| Close behavior | Session closes when user is inactive for 90 min |
| Processing | Expired sessions processed by Celery Beat |

---

## 7. Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER SENDS MESSAGE                       │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ChatView.post()                            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 1. get_or_create_session()                              │    │
│  │    → Creates/updates ChatSession in Django DB           │    │
│  └─────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 2. UserCoreMemory.to_prompt_string()                    │    │
│  │    → "Name: Daniel\nAge: 28\n..." (always present)     │    │
│  └─────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 3. retrieve_relevant_memories(user, message)            │    │
│  │    → embed(message) → Qdrant query → top 6 memories    │    │
│  │    → "[work | 2025-06-15] ..."                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 4. get_today_chats() → recent messages for context     │    │
│  └─────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 5. Build ultimate_info = core + episodic                │    │
│  └─────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 6. chat_service.answer() → LLM generates reply          │    │
│  │    (with personality + core memory + episodic memories  │    │
│  │     + daily context + user message)                     │    │
│  └─────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 7. Save user message + AI reply to Message table        │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                    (90 min pass)
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                Celery Beat (every 10 min)                        │
│                run_memory_extraction()                           │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ get_expired_unprocessed_sessions()                       │    │
│  │ → Finds sessions inactive >90 min, not yet extracted    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  For each session:                                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ process_session(session)                                 │    │
│  │  │                                                       │    │
│  │  ├── extract_episodic_memories()                         │    │
│  │  │     Transcript → LLM → JSON array of memories        │    │
│  │  │     For each: embed → Qdrant upsert + DB log         │    │
│  │  │                                                       │    │
│  │  ├── update_core_memory()                                │    │
│  │  │     Transcript + existing profile → LLM → JSON       │    │
│  │  │     Merge only changed fields → save                  │    │
│  │  │                                                       │    │
│  │  └── Mark session extracted                              │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                          │
                    (next chat message)
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│              CYCLE REPEATS — memory is now richer               │
│              Core profile updated + new episodic memories       │
│              available for semantic search                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference: Which File Does What

| File | Role |
|------|------|
| `memory/models.py` | Django models: CoreMemory, EpisodicMemoryLog, ChatSession, LongMemory |
| `memory/embeddings.py` | Text → 384-dim vector (sentence-transformers) |
| `memory/qdrant_client.py` | Qdrant connection + collection setup |
| `memory/episodic.py` | Store + retrieve episodic memories from Qdrant |
| `memory/extractor.py` | LLM extraction: episodic memories + core memory updates |
| `memory/session_tracker.py` | Session lifecycle: create, timeout, find expired |
| `memory/tasks.py` | Celery task: `run_memory_extraction` |
| `memory/logic.py` | Daily chat context for prompt |
| `chat/views.py` | `ChatView.post()` — orchestrates real-time memory retrieval |
| `chat/main.py` | Chat LLM — receives `ultimate_info` in prompt |
| `config/settings.py` | Celery Beat schedule, Qdrant/Redis config |
