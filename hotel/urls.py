from django.urls import path, include

from . import views

urlpatterns = [
    path("search/", views.search, name="search"),
    path("hotel/room/", views.room, name="add_room"),
    path("book/<int:room_id>/", views.book_room, name="book_room"),

    path('reservations/', views.reservations, name='reservations'),

    path( 'cancel/<int:reservation_id>/', views.cancel_reservation, name = "cancel_reservation" ),
    # path( 'hotels/<int:hotel_id>/', views.hotel_detail, name = "hotel_detail" ),
    # path( 'hotels/<int:hotel_id>/book/', views.book_hotel, name = "book_hotel" ),
    # path( 'hotels/<int:hotel_id>/book/success/', views.book_success, name = "book_success" ),
]
