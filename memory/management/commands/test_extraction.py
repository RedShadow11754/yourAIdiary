from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from memory.session_tracker import get_expired_unprocessed_sessions, get_or_create_session
from memory.extractor import process_session
from memory.models import ChatSession
from django.utils import timezone


class Command(BaseCommand):
    help = "Manually trigger memory extraction for a user (for testing)"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str)

    def handle(self, *args, **options):
        username = options["username"]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(f"User '{username}' not found.")
            return

        # Force-close any open session for this user
        session = ChatSession.objects.filter(
            user=user,
            memory_extracted=False
        ).order_by("-started_at").first()

        if not session:
            self.stdout.write(f"No unprocessed session found for '{username}'.")
            return

        self.stdout.write(f"Processing session {session.id} for {username}...")
        process_session(session)
        self.stdout.write("Done. Check your Qdrant and UserCoreMemory for results.")