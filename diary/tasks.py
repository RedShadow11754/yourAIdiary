from celery import shared_task
from django.contrib.auth.models import User
from django.utils import timezone
from .extractor import extract_diary_entry


@shared_task
def run_diary_extraction():
    """
    Runs at midnight every day.
    Loops through all users and extracts diary entries for today.
    """
    today = timezone.now().date()
    users = User.objects.filter(is_active=True)

    print(f"[Diary Task] Running extraction for {users.count()} users on {today}")

    for user in users:
        try:
            extract_diary_entry(user, today)
        except Exception as e:
            print(f"[Diary Task] Error for {user.username}: {e}")