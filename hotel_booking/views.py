from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from hotel import models


def index(request):
    if request.user.is_authenticated:
        user = request.user
        if (
            user.role == "client"
            and not models.Hotel.objects.filter(owner=user).exists()
        ):
            return redirect("hotel_signup")

    hotels = models.Hotel.objects.filter(is_active=True).order_by("?")[:6]
    rooms = models.Room.objects.filter(
        availability_status=models.Room.AvailabilityStatus.AVAILABLE,
    ).order_by("?")[:6]

    return render(request, "index.html", {"hotels": hotels, "rooms": rooms})


def about(request):
    return render(request, "about.html")


def explore_rooms(request):
    if request.method == "POST":
        search_query = request.POST.get("search", "")

        rooms = (
            models.Room.objects.filter(
                availability_status=models.Room.AvailabilityStatus.AVAILABLE,
            )
            .filter(
                Q(hotel__hotel_name__icontains=search_query)
                | Q(room_number__icontains=search_query)
                | Q(bed_configuration__icontains=search_query)
                | Q(amenities__icontains=search_query)
                | Q(view__icontains=search_query)
            )
            .select_related("hotel")
        )
    else:
        rooms = models.Room.objects.filter(
            availability_status=models.Room.AvailabilityStatus.AVAILABLE,
        ).select_related("hotel")

    paginator = Paginator(rooms, 9)  # Show 9 rooms per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "explore_rooms.html", {"rooms": page_obj})


def explore_hotels(request):
    if request.method == "POST":
        search_query = request.POST.get("search", "")

        hotels = models.Hotel.objects.filter(
            is_active=True,
        ).filter(
            Q(hotel_name__icontains=search_query)
            | Q(address__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(amenities__icontains=search_query)
        )
    else:
        hotels = models.Hotel.objects.filter(
            is_active=True,
        )

    paginator = Paginator(hotels, 9)  # Show 9 hotels per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "explore_hotels.html", {"hotels": page_obj})


@login_required(login_url="/login/")
def settings(request):
    return render(request, "accounts/settings.html")
