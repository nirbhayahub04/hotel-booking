"""
URL configuration for hotel_booking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'), )
"""

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views, settings


urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("", include("hotel.urls")),
    path("", include("client.urls")),
    path("", include("payments.urls")),
    path("", views.index, name="homepage"),
    path("about/", views.about, name="about"),
    path("explore/rooms", views.explore_rooms, name="explore_rooms"),
    path("explore/hotels", views.explore_hotels, name="explore_hotels"),
    path("settings/", views.settings, name="settings"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)