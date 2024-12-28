from django.shortcuts import render

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
