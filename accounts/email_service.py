from django.core.mail import send_mail
from django.conf import settings


def send_otp_email(to_email: str, username: str, otp_code: str) -> bool:
    """Send OTP email. Returns True if sent, False if failed.
    Does NOT raise exceptions — safe to call even if email isn't configured.
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
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"[Email] Failed to send OTP to {to_email}: {e}")
        return False