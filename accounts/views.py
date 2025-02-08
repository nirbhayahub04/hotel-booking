from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from hotel.models import HotelModel

from .forms import HotelSignUpForm, LoginForm, UserSignUpForm, ClientSignUpForm


def login_view( request ):
	msg = None
	form = LoginForm( request.POST or None )

	if request.user.is_authenticated:
		return redirect( "/" )

	if request.method == "POST":
		if form.is_valid():
			username = form.cleaned_data.get( "username" )
			password = form.cleaned_data.get( "password" )

			user = authenticate( username = username, password = password )

			if user is not None:
				login( request, user )

				if user.is_superuser:
					return redirect( "/admin" )

				if user.role == "client":
					if HotelModel.objects.filter( owner = user ).exists():
						return redirect( "/" )
					else:
						return redirect( "register_hotel" )

				return redirect( "/" )
			msg = "Invalid credentials"
		else:
			msg = "Error validating the form"

	return render( request, "login.html", { "form": form, "msg": msg } )


def register_user( request ):
	msg = None
	success = False

	if request.user.is_authenticated:
		return redirect( "/" )

	if request.method == "POST":
		form = UserSignUpForm( request.POST )

		if form.is_valid():
			user = form.save(commit = False)
			user.save()

			msg = "User created successfully."
			success = True

			return redirect( "login" )

		print(form.errors)

		msg = "Form is not valid"
	else:
		form = UserSignUpForm()

	return render(
		request,
		"register.html",
		{ "form": form, "msg": msg, "success": success },
	)


def register_hotel_owner( request ):
	msg = None
	success = False

	if request.method == "POST":
		if request.user.is_authenticated:
			return redirect( "/" )

		form = ClientSignUpForm( request.POST )

		if form.is_valid():
			user = form.save( commit = False )
			user.role = "client"
			user.save()

			msg = "User created successfully."
			success = True

			return redirect( "register_hotel" )

		msg = "Form is not valid"
	else:
		form = ClientSignUpForm()

	return render(
		request,
		"client/register.html",
		{ "form": form, "msg": msg, "success": success },
	)


@login_required()
def logout_user( request ):
	logout( request )
	return redirect( "/" )


@login_required()
def register_hotel( request ):
	msg = None
	success = False

	if request.user.role != "client":
		return redirect( "/" )

	if request.method == "POST":
		form = HotelSignUpForm( request.POST, request.FILES )

		if form.is_valid():
			hotel = form.save(commit = False)
			hotel.owner = request.user
			hotel.save()
   
			msg = "Hotel created successfully."
			success = True

			return redirect( "/" )

		msg = "Form is not valid"
	else:
		form = HotelSignUpForm()

	return render(
		request,
		"client/signup_hotel.html",
		{ "form": form, "msg": msg, "success": success },
	)