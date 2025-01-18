from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from . import models
from .forms import RoomForm


# Create your views here.
def search( request ):
	trips = { }

	searchParam = request.GET.get( 'q', 'default' )

	if searchParam != "default":
		trips = searchParam
	else:
		trips = ""

	return render(
		request,
		"search.html",
		{ "trips": trips }
	)


@login_required( login_url="/login/" )
def index( request ):
	if request.user.role == "client":
		hotel = models.HotelModel.objects.all().filter( owner=request.user )[
			0 ]
		rooms = models.RoomModel.objects.all().filter( hotel=hotel )

		return render( request, "client/rooms.html", { "hotel": hotel,
		                                               "rooms": rooms }
		               )

	return render( request, "404.html" )


@login_required( login_url="/login/" )
def room( request ):
	if request.user.role == "client":
		msg = None
		success = False

		hotel = models.HotelModel.objects.all().filter( owner=request.user )[
			0 ]
		rooms = models.RoomModel.objects.all().filter( hotel=hotel )

		if request.method == "POST":
			form = RoomForm( request.POST )

			if form.is_valid():
				hotel_room = form.save( commit=False )
				hotel_room.hotel = hotel
				hotel_room.save()

				msg = "User created successfully."
				success = True

				return redirect( "rooms" )

			msg = "Form is not valid"
		else:
			form = RoomForm()

		return render(
			request,
			"client/add_room.html",
			{ "form": form, "hotel": hotel,
			  "rooms": rooms, "msg": msg, "success": success },
		)

	return render( request, "404.html" )
