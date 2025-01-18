from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


@admin.register( models.HotelModel )
class HotelModelAdmin( admin.ModelAdmin ):
	empty_value_display = "-empty-"


@admin.register( models.RoomModel )
class RoomModelAdmin( admin.ModelAdmin ):
	empty_value_display = "-empty-"


@admin.register( models.ReservationModel )
class ReservationModelAdmin( admin.ModelAdmin ):
	empty_value_display = "-empty-"
