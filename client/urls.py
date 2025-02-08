from django.urls import path, include

from . import views


urlpatterns = [
    path("client/dashboard/", views.index, name="client-dashboard"),
    path("client/dashboard/tables", views.tables, name="tables"),
    path("client/dashboard/billing", views.billing, name="billing"),
    path("client/dashboard/profile", views.profile, name="profile"),
    
	
    path("client/dashboard/rooms", views.get_rooms, name="hotel_room"),
    path("client/dashboard/room", views.room, name="room"),
    path(
        "client/dashboard/room/remove/<int:id>", views.delete_room, name="delete_room"
    ),
    path(
        "client/dashboard/room/edit/<int:id>", views.edit_room, name="edit_room"
    ),
]
