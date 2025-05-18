from django.urls import path, include

from . import views


urlpatterns = [
    path("client/dashboard/", views.index, name="client-dashboard"),
    path("client/dashboard/tables", views.tables, name="tables"),
    path("client/dashboard/billing", views.billing, name="billing"),
    path("client/dashboard/profile", views.profile, name="profile"),
    path("client/dashboard/rooms", views.get_rooms, name="get_rooms"),
    path("client/dashboard/room", views.room, name="room"),
    path(
        "client/dashboard/room/remove/<int:room_id>",
        views.delete_room,
        name="delete_room",
    ),
    path("client/dashboard/room/edit/<int:room_id>", views.edit_room, name="edit_room"),
    path(
        "client/room/update-availibility/<int:room_id>",
        views.update_availibility,
        name="update_room_status",
    ),
    path(
        "client/dashboard/room/upload-image/<int:room_id>",
        views.upload_room_images,
        name="upload_room_images",
    ),
    path(
        "client/dashboard/room/delete-image/<int:image_id>",
        views.delete_room_image,
        name="delete_room_image",
    ),
    path(
        "client/dashboard/room/<int:room_id>/set-primary-image/<int:image_id>/",
        views.set_primary_room_image,
        name="set_primary_room_image",
    ),
    path(
        "client/dashboard/booked-rooms",
        views.client_booked_rooms,
        name="client_booked_rooms",
    ),
    path(
        "client/dashboard/billing-history",
        views.client_billing_history,
        name="client_billing_history",
    ),
    path(
        "client/dashboard/hotel-information",
        views.hotel_information,
        name="hotel_information",
    ),
    path(
        "client/dashboard/edit-hotel-information",
        views.edit_hotel_information,
        name="edit_hotel",
    ),
    path(
        "client/dashboard/set-primary-hotel-image/<int:image_id>",
        views.set_primary_hotel_image,
        name="set_primary_hotel_image",
    ),
    path(
        "client/dashboard/delete-hotel-image/<int:image_id>",
        views.delete_hotel_image,
        name="delete_hotel_image",
    ),
    path(
        "client/dashboard/upload-hotel-images",
        views.upload_hotel_images,
        name="upload_hotel_images",
    ),
]
