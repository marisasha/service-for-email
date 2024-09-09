from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.cache import caches
from django_app import models
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q
import imaplib
import email
from email.header import decode_header
import chardet


def login_user(request: HtttpRequest):
    if request.method == "GET":
        return render(request, "Login.html")
    elif request.method == "POST":
        username = str(request.POST["username"])
        password = str(request.POST["password"])
        user = authenticate(username=username, password=password)
        if user is None:
            return render(
                request,
                "Login.html",
                context={"error": "Логин или пароль не совпадают!"},
            )
        login(request, user)
        return redirect(reverse("home"))


def register(request: HtttpRequest):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        username = str(request.POST["username"])
        password = str(request.POST["password"])
        password_accept = str(request.POST["password_accept"])
        if password != password_accept:
            return render(
                request, "register.html", context={"error": "Пароли не совпадают!"}
            )
        user = User.objects.create(username=username, password=make_password(password))
        mail_username = str(request.POST["mail_username"])
        mail_password = str(request.POST["mail_password"])
        user_profile = models.Profile.objects.get(user=user)
        user_profile.mail_login = mail_username
        user_profile.mail_password = mail_password
        user_profile.save()
        login(request, user)
        return redirect(reverse("home"))


def logout_user(request: HtttpRequest):
    logout(request)
    return redirect(reverse("login"))


def home(request: HtttpRequest):
    return render(request=request, template_name="Home.html", context={})


def message(request: HtttpRequest):
    return render(request=request, template_name="Message.html", context={})
