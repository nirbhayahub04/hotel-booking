from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import redirect, render


def client_or_superuser_required( view_func ):
	@wraps( view_func )
	def _wrapped_view( request, *args, **kwargs ):
		if request.user.is_authenticated:
			if request.user.role == "client" or request.user.is_superuser:
				return view_func( request, *args, **kwargs )
		return render( request, "404.html" )


	return _wrapped_view
