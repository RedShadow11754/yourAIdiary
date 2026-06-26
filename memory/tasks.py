from celery import shared_task
from .session_tracker import get_expired_unprocessed_sessions
from .extractor import process_session


@shared_task
def run_memory_extraction():
    """
    Periodic task — runs every 10 minutes.
    Finds sessions that have been inactive for 90+ minutes
    and haven't been processed yet, then extracts memories.
    """
    sessions = get_expired_unprocessed_sessions()
    count = sessions.count()

    if count == 0:
        print("[Memory Task] No sessions to process.")
        return

    print(f"[Memory Task] Processing {count} expired session(s).")
    for session in sessions:
        try:
            process_session(session)
        except Exception as e:
            print(f"[Memory Task] Error processing session {session.id}: {e}")