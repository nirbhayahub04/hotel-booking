from tkinter.font import names

from django.shortcuts import render, redirect

from hotel.models import HotelModel, RoomModel
from hotel.forms import RoomForm

# Create your views here.
from hotel_booking.decorators import client_or_superuser_required


@client_or_superuser_required
def index( request ):
	return render( request, "client/index.html" )


@client_or_superuser_required
def tables( request ):
	return render( request, "client/tables.html" )


@client_or_superuser_required
def billing( request ):
	return render( request, "client/billing.html" )


@client_or_superuser_required
def profile( request ):
    hotel = HotelModel.objects.filter( owner=request.user ).first()
    return render( request, "client/profile.html", { "hotel": hotel } )


@client_or_superuser_required
def room( request ):
	form = RoomForm()

	if request.method == "POST":
		hotel = HotelModel.objects.all().filter( owner=request.user )[ 0 ]
		form = RoomForm( request.POST )

		if form.is_valid():
			room = form.save( commit=False )
			room.hotel = hotel
			room.save()

			return redirect( "hotel_room" )

	return render(
		request,
		"client/form.html",
		{ "form": form, "name": "Room" }
	)


@client_or_superuser_required
def get_rooms( request ):
	is_empty = False

	hotel = HotelModel.objects.all().filter(
		owner=request.user
	)[ 0 ]
	rooms = RoomModel.objects.all().filter( hotel=hotel )

	if rooms.count() == 0:
		is_empty = True

	return render(
		request,
		"client/room.html",
		{
			"rooms": rooms,
			"empty": is_empty
		}
	)


@client_or_superuser_required
def edit_room( request, id ):
	room = RoomModel.objects.get( id=id )
	form = RoomForm( instance=room )

	if request.method == "POST":
		form = RoomForm( request.POST, instance=room )
		if form.is_valid():
			form.save()
			return redirect( "hotel_room" )

	return render(
		request,
		"client/form.html",
		{ "form": form, "name": "Room" }
	)


@client_or_superuser_required
def delete_room( request, id ):
	hotel = HotelModel.objects.all().filter(
		owner=request.user
	)[ 0 ]
	res = RoomModel.objects.all().filter( hotel=hotel, id=id ).delete()

	return redirect( "hotel_room" )
