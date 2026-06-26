from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class LongMemory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()



class UserCoreMemory(models.Model):
    """
    The permanent, always-injected profile of a user.
    Updated (not appended) after each session by the extractor.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="core_memory")

    # Structured fast-access fields
    known_name = models.CharField(max_length=100, blank=True)
    age = models.CharField(max_length=20, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)

    # Freeform evolving fields — AI writes and rewrites these
    relationships = models.TextField(blank=True)   # "Sister: Maya, close but complicated. Best friend: Joe."
    personality_observations = models.TextField(blank=True)  # "Tends to overthink. Humor is dry."
    recurring_themes = models.TextField(blank=True)  # "Work stress, family tension, self-doubt."
    important_life_events = models.TextField(blank=True)  # "Lost job in March. Started therapy in April."
    current_life_context = models.TextField(blank=True)  # "Currently going through a breakup."

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - core memory"

    def to_prompt_string(self):
        """Formats the core memory into a clean string for prompt injection."""
        parts = []
        if self.known_name:
            parts.append(f"Name: {self.known_name}")
        if self.age:
            parts.append(f"Age: {self.age}")
        if self.occupation:
            parts.append(f"Occupation: {self.occupation}")
        if self.location:
            parts.append(f"Location: {self.location}")
        if self.relationships:
            parts.append(f"Key relationships: {self.relationships}")
        if self.personality_observations:
            parts.append(f"Personality: {self.personality_observations}")
        if self.recurring_themes:
            parts.append(f"Recurring themes in their life: {self.recurring_themes}")
        if self.important_life_events:
            parts.append(f"Important life events: {self.important_life_events}")
        if self.current_life_context:
            parts.append(f"Current life context: {self.current_life_context}")
        return "\n".join(parts) if parts else "No long-term memory yet for this user."


class EpisodicMemoryLog(models.Model):
    """
    A local log of every episodic memory stored in Qdrant.
    Lets you manage, archive, and reference memories without hitting Qdrant for admin.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="episodic_logs")
    qdrant_id = models.CharField(max_length=100, unique=True)  # UUID stored in Qdrant
    summary = models.TextField()  # Human-readable summary of what was stored
    category = models.CharField(max_length=50, blank=True)  # emotion, relationship, work, health, etc.
    session_date = models.DateField()
    last_referenced_at = models.DateTimeField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.category} | {self.session_date}"


class ChatSession(models.Model):
    """
    Tracks chat sessions for triggering the memory extraction pipeline.
    A session closes after 90 minutes of inactivity.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)
    memory_extracted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} | session {self.started_at.date()}"
