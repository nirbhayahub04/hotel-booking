from django.shortcuts import get_object_or_404, render, redirect
from client.forms import RoomForm
from hotel.models import Hotel, Room
from hotel_booking.decorators import client_or_superuser_required


@client_or_superuser_required
def index(request):
    return render(request, "client/index.html")


@client_or_superuser_required
def tables(request):
    return render(request, "client/tables.html")


@client_or_superuser_required
def billing(request):
    return render(request, "client/billing.html")


@client_or_superuser_required
def profile(request):
    hotel = Hotel.objects.filter(owner=request.user).first()
    return render(request, "client/profile.html", {"hotel": hotel})


@client_or_superuser_required
def room(request):
    form = RoomForm()
    hotel = Hotel.objects.filter(owner=request.user).first()

    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel
            room.save()
            return redirect("get_rooms")

        print(form.errors)

    return render(
        request,
        "client/forms/add_room.html",
        {
            "form": form,
        },
    )


@client_or_superuser_required
def get_rooms(request):
    is_empty = False
    hotel = Hotel.objects.filter(owner=request.user).first()
    rooms = Room.objects.filter(hotel=hotel)

    if rooms.count() == 0:
        is_empty = True

    return render(request, "client/room.html", {"rooms": rooms, "empty": is_empty})


@client_or_superuser_required
def edit_room(request, room_id):
    room = Room.objects.get(room_id=room_id)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("get_rooms")

    return render(request, "client/forms/add_room.html", {"form": form})


@client_or_superuser_required
def delete_room(request, room_id):
    hotel = Hotel.objects.filter(owner=request.user).first()
    Room.objects.filter(hotel=hotel, room_id=room_id).delete()
    return redirect("get_rooms")


def update_availibility(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)
    if request.method == "POST":
        data = request.POST
        room.availability_status = data["availability_status"]
        room.save()

        return redirect("get_rooms")
