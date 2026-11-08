from django.urls import path

from .views import (
    login_view,
    logout_view,
    register_view,
    send_otp,
    verify_email_token,
    verify_otp,
)

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("verify_token/<token>/", verify_email_token, name="verify_email_token"),
    path("send-otp/<email>/", send_otp, name="send_otp"),
    path("verify_otp/<email>/", verify_otp, name="verify_otp"),
    path("logout/", logout_view, name="logout"),
]
