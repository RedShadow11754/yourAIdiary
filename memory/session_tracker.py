from datetime import timedelta
from django.utils import timezone
from .models import ChatSession

SESSION_TIMEOUT_MINUTES = 90


def get_or_create_session(user):
    """
    Called on every incoming message.
    Returns the active session, or creates a new one if last session expired.
    """
    cutoff = timezone.now() - timedelta(minutes=SESSION_TIMEOUT_MINUTES)

    active_session = ChatSession.objects.filter(
        user=user,
        ended_at__isnull=True,
        last_activity_at__gte=cutoff
    ).order_by("-last_activity_at").first()

    if active_session:
        active_session.last_activity_at = timezone.now()
        active_session.save(update_fields=["last_activity_at"])
        return active_session
    else:
        # Close any lingering open session before creating a new one
        ChatSession.objects.filter(
            user=user,
            ended_at__isnull=True
        ).update(ended_at=timezone.now())

        return ChatSession.objects.create(
            user=user,
            last_activity_at=timezone.now()
        )


def get_expired_unprocessed_sessions():
    """
    Returns sessions that have been inactive for 90+ minutes
    and haven't had memory extracted yet.
    Used by the Celery beat task.
    """
    cutoff = timezone.now() - timedelta(minutes=SESSION_TIMEOUT_MINUTES)
    return ChatSession.objects.filter(
        ended_at__isnull=True,
        memory_extracted=False,
        last_activity_at__lte=cutoff
    )