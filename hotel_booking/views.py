from django.shortcuts import render

from hotel import models as hotelModel


def index( request ):
	"""Home page view"""

	hotels = hotelModel.HotelModel.objects.all()[ :3 ]
	rooms = hotelModel.RoomModel.objects.all()[ :3 ]

	return render(
		request,
		"index.html",
		{
			"hotels": hotels,
			"rooms": rooms
		}
	)


def about( request ):
	return render( request, "about.html" )


def explore( request ):
	rooms = hotelModel.RoomModel.objects.all()

	return render(
		request,
		"explore.html",
		{
			"rooms": rooms
		}
	)
