from django.db import models
from django.contrib.auth.models import User


class DiaryEntry(models.Model):

    MOOD_CHOICES = [
        ("happy", "Happy"),
        ("sad", "Sad"),
        ("angry", "Angry"),
        ("anxious", "Anxious"),
        ("excited", "Excited"),
        ("lonely", "Lonely"),
        ("peaceful", "Peaceful"),
        ("confused", "Confused"),
        ("grateful", "Grateful"),
        ("numb", "Numb"),
        ("hopeful", "Hopeful"),
        ("frustrated", "Frustrated"),
        ("melancholic", "Melancholic"),
        ("content", "Content"),
        ("overwhelmed", "Overwhelmed"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="diary_entries")
    date = models.DateField()  # The day this entry is about

    # Core content
    content = models.TextField()  # AI-generated, Anne Frank standard
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, default="other")

    # Narrative continuity thread — one sentence, updated every night
    narrative_thread = models.TextField(blank=True)

    # Edit support — for all users, frontend gates pro/free
    is_edited = models.BooleanField(default=False)
    edited_content = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "date")  # One entry per user per day
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.username} | {self.date} | {self.mood}"

    @property
    def display_content(self):
        """Always return edited content if it exists, otherwise original."""
        return self.edited_content if self.is_edited and self.edited_content else self.content