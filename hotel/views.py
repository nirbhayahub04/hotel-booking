import datetime
import re
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from . import models
from .forms import RoomForm


# Create your views here.
def search(request):
    trips = {}

    searchParam = request.GET.get("q", "default")

    if searchParam != "default":
        trips = searchParam
    else:
        trips = ""

    return render(request, "search.html", {"trips": trips})


@login_required(login_url="/login/")
def index(request):
    if request.user.role == "client":
        hotel = models.HotelModel.objects.all().filter(owner=request.user)[:1]
        rooms = models.RoomModel.objects.all().filter(hotel=hotel)

        return render(request, "client/rooms.html", {"hotel": hotel, "rooms": rooms})

    return render(request, "404.html")


@login_required(login_url="/login/")
def room(request):
    if request.user.role == "client":
        msg = None
        success = False

        hotel = models.HotelModel.objects.all().filter(owner=request.user)[:1]
        rooms = models.RoomModel.objects.all().filter(hotel=hotel)

        if request.method == "POST":
            form = RoomForm(request.POST)

            if form.is_valid():
                hotel_room = form.save(commit=False)
                hotel_room.hotel = hotel
                hotel_room.save()

                msg = "User created successfully."
                success = True

                return redirect("rooms")

            msg = "Form is not valid"
        else:
            form = RoomForm()

        return render(
            request,
            "client/add_room.html",
            {
                "form": form,
                "hotel": hotel,
                "rooms": rooms,
                "msg": msg,
                "success": success,
            },
        )

    return render(request, "404.html")


@login_required(login_url="/login/")
def book_room(request, room_id):
    if request.user.role == "client":
        return redirect("/")
    
    if request.method == "POST":
        room = models.RoomModel.objects.get(id=room_id)
        reservation = models.ReservationModel(
            reserved_by=request.user,
            check_in_date=request.POST["check_in"],
            check_out_date=request.POST["check_out"],
            room=room,
        )
        reservation.save()

        return redirect("/")
    elif request.method == "GET":
        room = models.RoomModel.objects.all().filter(id=room_id).first()
        return render(request, "booking.html", {"room": room})


@login_required(login_url="/login/")
def reservations(request):
    if request.user.role == "client":
        return redirect("/")

    reservations = models.ReservationModel.objects.all().filter(reserved_by=request.user)

    past_reservations = []
    upcoming_reservations = []
    
    today = datetime.date.today()
    
    for reservation in reservations:
        if reservation.check_out_date < today:
            past_reservations.append(reservation)
        else:
            upcoming_reservations.append(reservation)

    print(upcoming_reservations)

    return render(request, "accounts/reservations.html", {
        "past_reservations": past_reservations,
        "upcoming_reservations": upcoming_reservations
    })


@login_required(login_url="/login/")
def cancel_reservation(request, reservation_id):
    if request.user.role == "client":
        return redirect("/")

    reservation = models.ReservationModel.objects.get(id=reservation_id)

    if reservation:
        if reservation.reserved_by == request.user:
            reservation.delete()
            return redirect("/reservations")

    return redirect("/reservations/")