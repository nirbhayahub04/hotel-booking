import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotel_booking.settings")
django.setup()

from faker import Faker
from random import randint, choice
from decimal import Decimal
from datetime import timedelta, datetime
from hotel.models import Hotel, Room, Reservation
from accounts.models import CustomUser

fake = Faker()


def generate_phone_number():
    return fake.numerify(text="###########")


def populate_users(n):
    for _ in range(n):
        user = CustomUser.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password="password123",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role=choice(["client", "customer"]),
            phone_number=generate_phone_number(),
            address=fake.address(),
            dob=fake.date_of_birth(minimum_age=18, maximum_age=65),
        )
        user.save()


def populate_hotels(n):
    users = CustomUser.objects.filter(role="client")
    for _ in range(n):
        hotel = Hotel.objects.create(
            hotel_name=fake.company(),
            address=fake.address(),
            city=fake.city(),
            state=fake.state(),
            country=fake.country(),
            postal_code=fake.postcode(),
            latitude=Decimal(fake.latitude()),
            longitude=Decimal(fake.longitude()),
            phone_number=generate_phone_number(),
            email=fake.company_email(),
            website=fake.url(),
            star_rating=randint(1, 5),
            amenities=", ".join(fake.words(nb=10)),
            check_in_time=datetime.strptime("14:00", "%H:%M").time(),
            check_out_time=datetime.strptime("11:00", "%H:%M").time(),
            owner=choice(users),
        )
        hotel.save()


def populate_rooms(n):
    hotels = Hotel.objects.all()
    room_types = ["SINGLE", "DOUBLE", "SUITE", "DELUXE"]
    for _ in range(n):
        if hotels:
            hotel = choice(hotels)
            room = Room.objects.create(
                room_number=f"{fake.random_int(min=100, max=999)}",
                hotel=hotel,
                room_type=choice(room_types),
                bed_configuration=f"{randint(1, 2)} {choice(['King', 'Queen'])} Bed(s)",
                max_occupancy=randint(1, 4),
                amenities=", ".join(fake.words(nb=5)),
                bathroom_type=choice(
                    ["Private with shower", "Shared bathroom", "Ensuite"]
                ),
                base_price=Decimal(randint(50, 500)),
                floor_number=randint(1, 10),
                view=choice(
                    ["Ocean View", "City View", "Mountain View", "Garden View"]
                ),
                size=f"{randint(20, 50)} m²",
                smoking_policy=choice(["SMOKING", "NON_SMOKING"]),
                accessibility_features=(
                    ", ".join(fake.words(nb=3)) if choice([True, False]) else None
                ),
            )
            room.save()


def populate_reservations(n):
    users = CustomUser.objects.filter(role="customer")
    rooms = Room.objects.all()
    for _ in range(n):
        if users and rooms:
            room = choice(rooms)
            check_in = fake.date_between(start_date="today", end_date="+30d")
            check_out = check_in + timedelta(days=randint(1, 14))

            reservation = Reservation.objects.create(
                user=choice(users),
                room=room,
                hotel=room.hotel,
                check_in_date=check_in,
                check_out_date=check_out,
                number_of_guests=randint(1, room.max_occupancy),
                special_requests=fake.sentence() if choice([True, False]) else None,
                payment_status=choice(["PENDING", "PAID", "CANCELLED", "REFUNDED"]),
            )
            reservation.save()


if __name__ == "__main__":
    # Clear existing data
    Reservation.objects.all().delete()
    Room.objects.all().delete()
    Hotel.objects.all().delete()

    # Populate the database
    print("Creating users...")
    populate_users(20)

    print("Creating hotels...")
    populate_hotels(10)

    print("Creating rooms...")
    populate_rooms(50)

    print("Creating reservations...")
    populate_reservations(100)

    print("Database populated successfully!")
