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
]
