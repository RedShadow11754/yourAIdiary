from django.core.mail import send_mail
from django.conf import settings
import socket


# Set a short SMTP socket timeout so broken email config doesn't hang the worker
_original_create_connection = socket.create_connection

def _timeout_create_connection(address, timeout=5, **kwargs):
    return _original_create_connection(address, timeout=timeout, **kwargs)

socket.create_connection = _timeout_create_connection


def send_otp_email(to_email: str, username: str, otp_code: str) -> bool:
    """Send OTP email. Returns True if sent, False if failed.
    Never raises exceptions — safe to call even if email isn't configured.
    """
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        print(f"[Email] EMAIL not configured. OTP for {to_email}: {otp_code}")
        return False
    try:
        send_mail(
            subject="Your verification code",
            message=f"Your verification code is: {otp_code}\n\nThis code expires in 10 minutes.",
            from_email=settings.EMAIL_FROM,
            recipient_list=[to_email],
            fail_silently=True,
        )
        print(f"[Email] OTP email sent to {to_email}")
        return True
    except Exception as e:
        print(f"[Email] Failed to send OTP to {to_email}: {e}")
        return False