from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from diary.extractor import extract_diary_entry


class Command(BaseCommand):
    help = "Manually trigger diary extraction for a user (for testing)"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str)

    def handle(self, *args, **options):
        username = options["username"]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(f"User '{username}' not found.")
            return

        today = timezone.now().date()
        self.stdout.write(f"Extracting diary entry for {username} on {today}...")

        entry = extract_diary_entry(user, today)

        if entry:
            self.stdout.write(f"\nMood: {entry.mood}")
            self.stdout.write(f"\nNarrative thread: {entry.narrative_thread}")
            self.stdout.write(f"\n--- DIARY ENTRY ---\n")
            self.stdout.write(entry.content)
        else:
            self.stdout.write("No entry created. Check logs above for reason.")