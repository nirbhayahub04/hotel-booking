from django.shortcuts import get_object_or_404, render, redirect
from client.forms import RoomForm
from hotel.forms import BasicInformationForm, FullForm, HotelImageForm, RoomImageForm
from hotel.models import Hotel, HotelImage, Reservation, Room, RoomImage
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
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel
            room.save()

            # Save multiple images
            images = request.FILES.getlist("images")
            for image in images:
                RoomImage.objects.create(room=room, image=image)

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


@client_or_superuser_required
def upload_room_images(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)
    if request.method == "POST":
        form = RoomImageForm(request.POST, request.FILES)
        if form.is_valid():
            images = form.cleaned_data["images"]
            for image in images:
                RoomImage.objects.create(room=room, image=image)
            if room.image == "images/rooms/default.jpg":
                random_image = (
                    RoomImage.objects.filter(room=room)
                    .exclude(image="images/rooms/default.jpg")
                    .order_by("?")
                    .first()
                )
                if random_image:
                    room.image = random_image.image
                    room.save()
            return redirect("get_rooms")
    else:
        form = RoomImageForm()

    return render(
        request, "client/forms/upload_room_images.html", {"form": form, "room": room}
    )


@client_or_superuser_required
def delete_room_image(request, image_id):
    image = get_object_or_404(RoomImage, id=image_id)
    image.delete()
    return redirect("get_rooms")


@client_or_superuser_required
def set_primary_room_image(request, room_id, image_id):
    room = get_object_or_404(Room, room_id=room_id)
    primary_image = get_object_or_404(RoomImage, id=image_id)

    # Update the room's primary image
    room.image = primary_image.image
    room.save()

    return redirect("get_rooms")


@client_or_superuser_required
def client_booked_rooms(request):
    booked_rooms = Reservation.objects.filter(
        hotel__owner=request.user,
        room__availability_status="BOOKED",
    ).select_related("room", "hotel")
    return render(request, "client/booked_rooms.html", {"rooms": booked_rooms})


@client_or_superuser_required
def client_billing_history(request):
    billing_records = (
        Reservation.objects.filter(hotel__owner=request.user)
        .select_related(
            "payment_ref_id",
            "room",
            "user",
        )
        .order_by("-booking_date")
    )  # Show most recent first

    return render(
        request,
        "client/billing_history.html",
        {"billing_records": billing_records, "total_records": billing_records.count()},
    )


@client_or_superuser_required
def hotel_information(request):
    hotel = get_object_or_404(Hotel, owner=request.user)
    hotel_images = HotelImage.objects.filter(hotel=hotel)
    return render(
        request,
        "client/hotel_information.html",
        {"hotel": hotel, "hotel_images": hotel_images},
    )


@client_or_superuser_required
def edit_hotel_information(request):
    hotel = get_object_or_404(Hotel, owner=request.user)

    if request.method == "POST":
        form = FullForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect("hotel_information")
    else:
        form = FullForm(instance=hotel)

    return render(
        request, "client/edit_hotel_information.html", {"form": form, "hotel": hotel}
    )


@client_or_superuser_required
def set_primary_hotel_image(request, image_id):
    hotel = get_object_or_404(Hotel, owner=request.user)
    image = get_object_or_404(HotelImage, id=image_id, hotel=hotel)

    # Set all images to not primary first
    HotelImage.objects.filter(hotel=hotel).update(is_primary=False)

    # Set selected image as primary
    image.is_primary = True
    image.save()

    # Update hotel's main image field
    hotel.image = image.image
    hotel.save()

    return redirect("hotel_information")


@client_or_superuser_required
def delete_hotel_image(request, image_id):
    hotel = get_object_or_404(Hotel, owner=request.user)
    image = get_object_or_404(HotelImage, id=image_id, hotel=hotel)

    # Check if this is the primary image
    was_primary = image.is_primary

    image.image.delete()
    image.delete()

    if was_primary:
        remaining_images = HotelImage.objects.filter(hotel=hotel)
        if remaining_images.exists():
            new_primary = remaining_images.first()
            new_primary.is_primary = True
            new_primary.save()

    return redirect("hotel_information")


@client_or_superuser_required
def upload_hotel_images(request):
    hotel = get_object_or_404(Hotel, owner=request.user)

    if request.method == "POST":
        images = request.FILES.getlist("images")
        for image in images:
            HotelImage.objects.create(hotel=hotel, image=image)
        return redirect("hotel_information")

    return render(request, "client/upload_hotel_images.html")
