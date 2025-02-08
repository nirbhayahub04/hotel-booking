from django.db import models

import accounts.models


# Create your models here.
class HotelModel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to="images/hotels", default="images/hotels/default.jpg"
    )
    description = models.TextField(default="No description")
    rating = models.FloatField(default=5)
    no_of_rooms = models.IntegerField(default=30)
    owner = models.ForeignKey(accounts.models.CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class RoomModel(models.Model):
    room_number = models.CharField(max_length=10)
    hotel = models.ForeignKey(HotelModel, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=50)
    price = models.IntegerField()
    image = models.ImageField(
        upload_to="images/rooms", default="images/rooms/default.jpg"
    )
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.hotel.name + "_" + self.room_number


class ReservationModel(models.Model):
    reserved_by = models.ForeignKey(
        accounts.models.CustomUser, on_delete=models.CASCADE
    )
    no_of_guests = models.IntegerField()
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    room = models.ForeignKey(RoomModel, on_delete=models.CASCADE)
