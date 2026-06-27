from django.db import models
from django.db import models
from django.contrib.auth.models import User
import random
import string
from django.utils import timezone
from datetime import timedelta


class OTPVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at

    @classmethod
    def generate_for_user(cls, user):
        # Invalidate any previous unused OTPs for this user
        cls.objects.filter(user=user, is_used=False).update(is_used=True)
        code = ''.join(random.choices(string.digits, k=6))
        return cls.objects.create(
            user=user,
            code=code,
            expires_at=timezone.now() + timedelta(minutes=10)
        )

    def __str__(self):
        return f"{self.user.username} | {self.code} | valid: {self.is_valid()}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - verified: {self.is_email_verified}"

# Create your models here.
