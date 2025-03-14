from django.urls import path, include

from . import views
from .forms import (
    AmenitiesForm,
    BasicInformationForm,
    HotelImageForm,
    LocationForm,
    PoliciesForm,
)

FORMS = [
    ("basic", BasicInformationForm),
    ("location", LocationForm),
    ("amenities", AmenitiesForm),
    ("policies", PoliciesForm),
    ("images", HotelImageForm),
]

urlpatterns = [
    path("signup/hotel", views.HotelSignupWizard.as_view(FORMS), name="hotel_signup"),
    path("search/", views.search, name="search"),
    path("room/<int:room_id>", views.get_room_detail, name="get_room_detail"),
    path("book/<int:room_id>/", views.book_room, name="book_room"),
    path("initiate-booking/", views.initiate_booking, name="initiate_booking"),
    path("bookings/", views.get_bookings, name="get_bookings"),
    path(
        "cancel/<int:reservation_id>/",
        views.cancel_booking,
        name="cancel_booking",
    ),
    path("hotels/<int:id>/", views.hotel_detail, name="hotel_detail"),
    # path( 'hotels/<int:hotel_id>/book/', views.book_hotel, name = "book_hotel" ),
    # path( 'hotels/<int:hotel_id>/book/success/', views.book_success, name = "book_success" ),
]
