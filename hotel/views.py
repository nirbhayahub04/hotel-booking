import datetime
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from formtools.wizard.views import SessionWizardView
from django.db import transaction
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.core.cache import cache

from client.forms import RoomForm

from . import models
from .forms import (
    BasicInformationForm,
    HotelImageForm,
    LocationForm,
    AmenitiesForm,
    PoliciesForm,
)


# Create your views here.
def search(request):
    trips = {}

    searchParam = request.GET.get("q", "default")

    if searchParam != "default":
        trips = searchParam
    else:
        trips = ""

    return render(request, "search.html", {"trips": trips})


def get_room_detail(request, room_id):
    room = get_object_or_404(models.Room, room_id=room_id)
    return render(request, "room_detail.html", {"room": room})


@login_required(login_url="/login/")
def book_room(request, room_id):
    if request.user.role == "client":
        return redirect("/")

    if request.method == "POST":
        # room = models.RoomModel.objects.get(id=room_id)
        # reservation = models.ReservationModel(
        #     reserved_by=request.user,
        #     check_in_date=request.POST["check_in"],
        #     check_out_date=request.POST["check_out"],
        #     room=room,
        # )
        # reservation.save()

        return redirect("/")
    elif request.method == "GET":
        room = models.Room.objects.filter(room_id=room_id).first()
        return render(request, "booking.html", {"room": room})


@login_required(login_url="/login/")
def get_bookings(request):
    if request.user.role == "client":
        return redirect("/")

    reservations = models.Reservation.objects.filter(user=request.user)

    past_reservations = []
    upcoming_reservations = []

    today = datetime.date.today()

    for reservation in reservations:
        if reservation.check_out_date < today:
            past_reservations.append(reservation)
        else:
            upcoming_reservations.append(reservation)

    return render(
        request,
        "accounts/reservations.html",
        {
            "past_reservations": past_reservations,
            "upcoming_reservations": upcoming_reservations,
        },
    )


@login_required(login_url="/login/")
def cancel_booking(request, reservation_id):
    if request.user.role == "client":
        return redirect("/")

    reservation = get_object_or_404(models.Reservation, reservation_id=reservation_id)

    if reservation:
        if reservation.user == request.user:
            reservation.delete()
            return redirect("get_bookings")

    return redirect("get_bookings")


def hotel_detail(request, id):
    hotel = get_object_or_404(models.Hotel, hotel_id=id)
    related_hotels = models.Hotel.objects.exclude(hotel_id=hotel.hotel_id).order_by(
        "?"
    )[:6]
    rooms = models.Room.objects.filter(hotel=hotel)
    hotel_images = models.HotelImage.objects.filter(hotel=hotel)

    return render(
        request,
        "hotel_detail.html",
        {
            "hotel": hotel,
            "related_hotels": related_hotels,
            "rooms": rooms,
            "hotel_images": hotel_images,
        },
    )


def initiate_booking(request):
    if request.method == "POST":
        data = request.POST
        payment_method = data["payment_method"]

        data = {
            "initiated_by": request.user.id,
            "room_id": data["room_id"],
            "check_in": data["check_in"],
            "check_out": data["check_out"],
            "no_of_guest": data["guests"],
            "special_requests": data["special_requests"],
        }
        cache.set("booking_data", data, 300000)

        if payment_method == "khalti":
            return redirect("pay_with_khalti")
        elif payment_method == "esewa":
            return redirect("pay_with_esewa")
        elif payment_method == "credit_card":
            print("Credit/Debit Card")
        else:
            return redirect("/")

    return redirect("/")


class HotelSignupWizard(SessionWizardView):
    TEMPLATES = {
        "basic": "client/hotel_signup/basic.html",
        "location": "client/hotel_signup/location.html",
        "amenities": "client/hotel_signup/amenities.html",
        "policies": "client/hotel_signup/policies.html",
        "images": "client/hotel_signup/hotel_images.html",
    }

    form_list = [
        ("basic", BasicInformationForm),
        ("location", LocationForm),
        ("amenities", AmenitiesForm),
        ("policies", PoliciesForm),
        ("images", HotelImageForm),
    ]

    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, "wizard_temp")
    )

    def get_template_names(self):
        return [self.TEMPLATES[self.steps.current]]

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login/")
        return super().dispatch(request, *args, **kwargs)

    def process_step_files(self, form):
        files = super().process_step_files(form)

        if "images-images" in files:
            new_files = files.getlist("images-images")
            saved_filenames = []

            for new_file in new_files:
                tmp_filename = self.file_storage.save(new_file.name, new_file)
                saved_filenames.append(tmp_filename)

            existing_filenames = self.storage.data.get("accumulated_images", [])
            combined_filenames = existing_filenames + saved_filenames

            self.storage.data["accumulated_images"] = combined_filenames

            del files["images-images"]

        return files

    def get_form_instance(self, step):
        instance = super().get_form_instance(step)

        if step == "images_step":
            stored_files = self.storage.get_step_files(step) or {}

            if "images" in stored_files:
                instance.cleaned_data["images"] = stored_files["images"]

        return instance

    def done(self, form_list, **kwargs):
        try:
            with transaction.atomic():
                hotel = self.process_forms(form_list)
                return render(
                    self.request, "client/hotel_signup/done.html", {"hotel": hotel}
                )
        except Exception as e:
            return render(
                self.request, "client/hotel_signup/error.html", {"error": str(e)}
            )

    def process_forms(self, form_list):
        hotel_forms = form_list[:-1]
        image_form = form_list[-1]

        hotel_data = {}
        for form in hotel_forms:
            hotel_data.update(form.cleaned_data)
        hotel = models.Hotel.objects.create(owner=self.request.user, **hotel_data)

        image_filenames = self.storage.data.get("accumulated_images", [])

        primary_index = image_form.cleaned_data.get("primary_image_index", -1)
        for idx, filename in enumerate(image_filenames):
            self.process_image(hotel, filename, idx == primary_index)

        for filename in image_filenames:
            self.file_storage.delete(filename)

        return hotel

    def process_image(self, hotel, filename, is_primary):
        with self.file_storage.open(filename) as f:
            content = f.read()
            original_name = os.path.basename(filename)
            file = ContentFile(content, name=original_name)
            models.HotelImage.objects.create(
                hotel=hotel,
                image=file,
                is_primary=is_primary,
                caption=f"Image {models.HotelImage.objects.filter(hotel=hotel).count() + 1}",
            )
            if is_primary:
                hotel.image = file
                hotel.save()

            file.close()
