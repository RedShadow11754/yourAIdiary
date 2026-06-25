from django.db import models
from django.contrib.auth.models import User

# Create your models here.




# Raw chat histories
class Message(models.Model):

    ROLE_CHOICES = [
        ("user", "User"),
        ("ai", "AI"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    # AI pipelines
    memory_processed = models.BooleanField(default=False)
    diary_processed = models.BooleanField(default=False)
    day = models.DateField(auto_now_add=True)

    # soft delete if needed later
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]





# Personality prompts
class PersonalityPrompt(models.Model):

    PERSONALITY_CHOICES = [
        ("sassiness", "Sassiness"),
        ("warmth", "Warmth"),
        ("banter", "Banter"),
        ("directness", "Directness"),
        ("verbosity", "Verbosity"),
        ("emoji", "Emoji Usage"),
    ]

    LEVEL_CHOICES = [
        (1, "Low"),
        (2, "Medium"),
        (3, "High"),
    ]

    personality = models.CharField(
        max_length=50,
        choices=PERSONALITY_CHOICES
    )

    level = models.IntegerField(
        choices=LEVEL_CHOICES,
    )

    prompt = models.TextField()

    class Meta:
        unique_together = ("personality", "level")

    def __str__(self):
        return f"{self.personality} - {self.level}"

    class Meta:
        unique_together = ("personality", "level")



# User personality
class UserPersonality(models.Model):

    LEVEL_CHOICES = [
        (1, "Low"),
        (2, "Medium"),
        (3, "High"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(default="user", max_length=50)

    sassiness = models.IntegerField(choices=LEVEL_CHOICES, default=2)
    warmth = models.IntegerField(choices=LEVEL_CHOICES, default=2)
    banter = models.IntegerField(choices=LEVEL_CHOICES, default=2)
    directness = models.IntegerField(choices=LEVEL_CHOICES, default=2)
    verbosity = models.IntegerField(choices=LEVEL_CHOICES, default=2)
    emoji = models.IntegerField(choices=LEVEL_CHOICES, default=2)

    custom_prompt = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} personality"