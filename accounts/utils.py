import uuid

from django.conf import settings
from django.core.mail import send_mail


def generateRandomToken():
    return str(uuid.uuid4())


def sendEmailToken(email, token):

    subject = "Verify your email address"
    message = f"""Hi Please verify your email by clicking this link
    http://127.0.0.1:8000/accounts/verify_token/{token}
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


def sendLoginOTP(email, otp):

    subject = "Login OTP"
    message = f"""Here is the OTP to Login
    {otp}
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
