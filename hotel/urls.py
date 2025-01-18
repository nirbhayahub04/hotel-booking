from django.urls import path, include

from . import views

urlpatterns = [
	path( 'search/', views.search, name = "search" ),

	path( 'hotel/', views.index, name = "rooms" ),

	path('hotel/room/', views.room, name = "add_room"),
	# path( 'hotels/<int:hotel_id>/', views.hotel_detail, name = "hotel_detail" ),
	# path( 'hotels/<int:hotel_id>/book/', views.book_hotel, name = "book_hotel" ),
	# path( 'hotels/<int:hotel_id>/book/success/', views.book_success, name = "book_success" ),
]
