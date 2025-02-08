import os
import django
from faker import Faker
from random import randint, choice
from decimal import Decimal
from datetime import timedelta
from hotel.models import HotelModel, RoomModel, ReservationModel
from accounts.models import CustomUser

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotel_booking.settings")
django.setup()

fake = Faker()

def populate_users(n):
    for _ in range(n):
        user = CustomUser.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password='password123',
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role=choice(['client', 'customer'])
        )
        user.save()

def populate_hotels(n):
    for _ in range(n):
        hotel = HotelModel.objects.create(
            name=fake.company(),
            address=fake.address(),
            image=fake.image_url(),
            description=fake.text(),
            rating=randint(1, 5),
            no_of_rooms=randint(10, 100),
            owner=CustomUser.objects.order_by('?').first()  # Randomly assign an owner
        )
        hotel.save()

def populate_rooms(n):
    hotels = HotelModel.objects.all()
    for _ in range(n):
        if hotels:
            room = RoomModel.objects.create(
                room_number=fake.random_int(min=100, max=999),
                hotel=choice(hotels),
                room_type=choice(['Single', 'Double', 'Suite']),
                price=randint(50, 500),
                image=fake.image_url(),
                capacity=randint(1, 4),
                is_available=choice([True, False])
            )
            room.save()

def populate_reservations(n):
    users = CustomUser.objects.all()
    rooms = RoomModel.objects.all()
    for _ in range(n):
        if users and rooms:
            reservation = ReservationModel.objects.create(
                reserved_by=choice(users),
                no_of_guests=randint(1, 4),
                check_in_date=fake.date_between(start_date='today', end_date='+30d'),
                check_out_date=fake.date_between(start_date='+31d', end_date='+60d'),
                room=choice(rooms)
            )
            reservation.save()


if __name__ == "__main__":
    # Populate the database
    populate_users(10)
    populate_hotels(5)
    populate_rooms(20)
    populate_reservations(15)
