from django.core.mail import send_mail
from django.conf import settings


def send_otp_email(to_email: str, username: str, otp_code: str):
    send_mail(
        subject="Your verification code",
        message=f"Your verification code is: {otp_code}\n\nThis code expires in 10 minutes.",
        from_email=settings.EMAIL_FROM,
        recipient_list=[to_email],
        fail_silently=False,
    )