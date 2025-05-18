from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from hotel.models import Hotel

from .forms import (
    HotelSignUpForm,
    LoginForm,
    UserSignUpForm,
    ClientSignUpForm,
)


def login_view(request):
    msg = None
    form = LoginForm(request.POST or None)

    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                if user.is_superuser:
                    return redirect("/admin")

                if user.role == "client":
                    if Hotel.objects.filter(owner=user).exists():
                        return redirect("/")
                    return redirect("hotel_signup")

                return redirect("/")
            msg = "Invalid credentials"
        else:
            msg = "Error validating the form"

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = UserSignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            msg = "User created successfully."
            success = True

            return redirect("login")

        msg = "Form is not valid"
    else:
        form = UserSignUpForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form, "msg": msg, "success": success},
    )


def register_hotel_owner(request):
    msg = None
    success = False

    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = ClientSignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.role = "client"
            user.save()

            msg = "User created successfully."
            success = True

            # Authenticate and login the user
            user = authenticate(
                username=user.username, password=form.cleaned_data["password1"]
            )
            if user is not None:
                login(request, user)
                return redirect("hotel_signup")

        msg = "Form is not valid"
    else:
        form = ClientSignUpForm()

    return render(
        request,
        "client/register.html",
        {"form": form, "msg": msg, "success": success},
    )


@login_required(login_url="/login")
def logout_user(request):
    logout(request)
    return redirect("/")


@login_required(login_url="/login")
def register_hotel(request):
    msg = None
    success = False

    if request.user.role != "client":
        return redirect("/")

    if request.method == "POST":
        form = HotelSignUpForm(request.POST, request.FILES)

        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.owner = request.user
            hotel.save()

            msg = "Hotel created successfully."
            success = True

            return redirect("/")

        msg = "Form is not valid"
    else:
        form = HotelSignUpForm()

    return render(
        request,
        "client/signup_hotel.html",
        {"form": form, "msg": msg, "success": success},
    )


@login_required(login_url="/login/")
def delete_account(request):
    if (
        request.user.role == "customer"
        and request.user.is_authenticated
        and request.user.is_active
        and not request.user.is_superuser
    ):
        if request.method == "POST":
            request.user.delete()
            return redirect("logout")

    return render(request, "accounts/settings.html")
