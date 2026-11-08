import random
from smtplib import SMTPException

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import HotelUser
from .utils import generateRandomToken, sendEmailToken, sendLoginOTP


# Create your views here.
def logout_view(request):
    logout(request)
    return redirect("login")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        hotel_user = HotelUser.objects.filter(email=email)

        if not hotel_user.exists():
            messages.error(request, "Account Not Found")
            return redirect("login")

        if not hotel_user[0].is_verified:
            messages.error(request, "Account is not Verified")
            return redirect("login")

        hotel_user = authenticate(username=hotel_user[0].username, password=password)

        if not hotel_user:
            messages.error(request, "Incorrect Credentials.")
            return redirect("login")

        messages.success(request, "Login Success")
        login(request, hotel_user)
        return redirect("/")

    return render(request, "accounts/login.html")


def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        password = request.POST.get("password")

        hotel_user = HotelUser.objects.filter(
            Q(email=email) | Q(phone_number=phone_number)
        )

        if hotel_user.exists():
            messages.error(
                request, "Account already exists with email or phone number."
            )
            return redirect("register")
        hotel_user = HotelUser.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone_number=phone_number,
            email=email,
            email_token=generateRandomToken(),
        )
        hotel_user.set_password(password)
        hotel_user.save()

        try:
            sendEmailToken(email, hotel_user.email_token)
            messages.success(request, "Verification email sent successfully.")
        except SMTPException as error:
            print("Email sending failed:", repr(error))
            messages.error(
                request, "Account created, but verification email could not be sent."
            )
        return redirect("register")
    # messages = {"tags": "warning", "messages": ["hello from warning"]}
    return render(request, "accounts/register.html")


def verify_email_token(request, token):
    try:
        hotel_user = HotelUser.objects.get(email_token=token)
        hotel_user.is_verified = True
        hotel_user.save()
        messages.success(request, "Email Verified")
        return redirect("login")
    except HotelUser.DoesNotExist:
        return HttpResponse("Invalid Token")


def send_otp(request, email):
    try:
        hotel_user = HotelUser.objects.get(email=email)

    except HotelUser.DoesNotExist:
        messages.error(request, "Account Not Found")
        return redirect("login")

    otp = random.randint(1000, 9999)
    hotel_user.otp = otp
    hotel_user.save()
    sendLoginOTP(email, otp)
    return redirect(f"/accounts/verify_otp/{email}")


def verify_otp(request, email):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        otp = request.POST.get("otp")

        try:
            hotel_user = HotelUser.objects.get(email=email)

        except HotelUser.DoesNotExist:
            messages.error(request, "Account Not Found")
            return redirect("login")

        if not hotel_user.is_verified:
            messages.error(request, "Account is not verified")
            return redirect("login")

        if str(hotel_user.otp) == str(otp):
            hotel_user.otp = None
            hotel_user.save(update_fields=["otp"])

            login(request, hotel_user)

            messages.success(request, "Login Success")
            return redirect("home")

        messages.error(request, "Invalid OTP")
        return redirect("verify_otp", email=email)

    return render(request, "accounts/otp-login.html")
