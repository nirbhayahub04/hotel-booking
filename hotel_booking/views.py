from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from hotel import models


def index(request):
    if request.user.is_authenticated:
        user = request.user
        if (
            user.role == "client"
            and not models.Hotel.objects.filter(owner=user).exists()
        ):
            return redirect("hotel_signup")

    hotels = models.Hotel.objects.filter(is_active=True).order_by("?")[:3]
    rooms = models.Room.objects.filter(
        availability_status=models.Room.AvailabilityStatus.AVAILABLE,
    ).order_by("?")[:3]

    return render(request, "index.html", {"hotels": hotels, "rooms": rooms})


def about(request):
    return render(request, "about.html")


def explore(request):
    rooms = models.Room.objects.filter(
        availability_status=models.Room.AvailabilityStatus.AVAILABLE,
    ).select_related("hotel")

    return render(request, "explore.html", {"rooms": rooms})


@login_required(login_url="/login/")
def settings(request):
    return render(request, "accounts/settings.html")
