from datetime import timezone
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

import accounts.models
from payments.models import PaymentHistory


class Hotel(models.Model):
    class Meta:
        verbose_name = _("Hotel")
        verbose_name_plural = _("Hotels")
        ordering = ["hotel_name"]
        indexes = [
            models.Index(fields=["city", "state"]),
            models.Index(fields=["star_rating"]),
        ]

    # Hotel Identification
    hotel_id = models.AutoField(
        primary_key=True,
        verbose_name=_("Hotel ID"),
        help_text=_("Unique identifier for the hotel"),
    )
    hotel_name = models.CharField(
        max_length=200,
        verbose_name=_("Hotel Name"),
        help_text=_("Official name of the hotel"),
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("Detailed description of the hotel"),
    )

    # Primary Image
    image = models.ImageField(
        upload_to="images/hotels/",
        verbose_name=_("Primary Image"),
        help_text=_("Main image of the hotel"),
        default="images/hotels/default.jpg",
    )

    # Location
    address = models.CharField(
        max_length=200,
        verbose_name=_("Address"),
        help_text=_("Street address of the hotel"),
    )
    city = models.CharField(
        max_length=100,
        verbose_name=_("City"),
        help_text=_("City where the hotel is located"),
    )
    state = models.CharField(
        max_length=100,
        verbose_name=_("State/Province"),
        help_text=_("State or province where the hotel is located"),
    )
    country = models.CharField(
        max_length=100,
        verbose_name=_("Country"),
        help_text=_("Country where the hotel is located"),
    )
    postal_code = models.CharField(
        max_length=20,
        verbose_name=_("Postal Code"),
        help_text=_("Postal or ZIP code of the hotel's location"),
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name=_("Latitude"),
        help_text=_("Geographical latitude coordinate"),
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name=_("Longitude"),
        help_text=_("Geographical longitude coordinate"),
    )

    # Contact Information
    phone_number = models.CharField(
        max_length=20,
        verbose_name=_("Phone Number"),
        help_text=_("Primary contact number for the hotel"),
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name=_("Email"),
        help_text=_("Primary email address for the hotel"),
    )
    website = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Website"),
        help_text=_("Official website of the hotel"),
    )

    # Hotel Features
    star_rating = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_("Star Rating"),
        help_text=_("Official star rating (1-5 stars)"),
    )
    amenities = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Amenities"),
        help_text=_("List of available amenities (comma-separated)"),
    )
    check_in_time = models.TimeField(
        default="15:00",
        verbose_name=_("Check-in Time"),
        help_text=_("Standard check-in time"),
    )
    check_out_time = models.TimeField(
        default="11:00",
        verbose_name=_("Check-out Time"),
        help_text=_("Standard check-out time"),
    )

    # Metadata
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Creation Date"),
        help_text=_("Date when the hotel was added to the system"),
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Last Updated"),
        help_text=_("Date when the hotel information was last updated"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Indicates if the hotel is currently active in the system"),
    )

    # Owner
    owner = models.ForeignKey(
        accounts.models.CustomUser,
        on_delete=models.CASCADE,
        related_name="hotels",
        verbose_name=_("Owner"),
        help_text=_("User who owns this hotel"),
    )

    def __str__(self):
        return f"{self.hotel_name} ({self.city}, {self.country})"


class Room(models.Model):
    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")
        ordering = ["room_number"]
        indexes = [
            models.Index(fields=["room_type"]),
            models.Index(fields=["availability_status"]),
        ]

    # Room Identification
    room_id = models.BigAutoField(
        primary_key=True,
        verbose_name=_("Room ID"),
        help_text=_("Unique identifier for the room"),
    )

    # Room Number
    room_number = models.CharField(
        max_length=10,
        verbose_name=_("Room Number"),
        help_text=_("Room Number of Hotel"),
    )

    # Hotel
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="rooms",
        verbose_name=_("Hotel"),
        help_text=_("The hotel this room belongs to"),
    )

    # Primary Image
    image = models.ImageField(
        upload_to="images/rooms/",
        verbose_name=_("Primary Image"),
        help_text=_("Main image of the room"),
        default="images/rooms/default.jpg",
    )

    # Room Type
    class RoomType(models.TextChoices):
        SINGLE = "SINGLE", _("Single")
        DOUBLE = "DOUBLE", _("Double")
        SUITE = "SUITE", _("Suite")
        DELUXE = "DELUXE", _("Deluxe")

    room_type = models.CharField(
        max_length=10,
        choices=RoomType.choices,
        verbose_name=_("Room Type"),
        help_text=_("Type of the room"),
    )
    bed_configuration = models.CharField(
        max_length=100,
        verbose_name=_("Bed Configuration"),
        help_text=_("Bed arrangement in the room"),
    )
    max_occupancy = models.PositiveIntegerField(
        verbose_name=_("Maximum Occupancy"),
        help_text=_("Maximum number of guests allowed"),
    )

    # Amenities
    amenities = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Amenities"),
        help_text=_("Comma-separated list of room amenities"),
    )
    bathroom_type = models.CharField(
        max_length=100,
        verbose_name=_("Bathroom Type"),
        help_text=_("Type of bathroom in the room"),
    )

    # Pricing
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Base Price"),
        help_text=_("Standard price for the room"),
    )

    # Availability
    class AvailabilityStatus(models.TextChoices):
        AVAILABLE = "AVAILABLE", _("Available")
        BOOKED = "BOOKED", _("Booked")
        MAINTENANCE = "MAINTENANCE", _("Under Maintenance")

    availability_status = models.CharField(
        max_length=20,
        choices=AvailabilityStatus.choices,
        default=AvailabilityStatus.AVAILABLE,
        verbose_name=_("Availability Status"),
    )
    booking_dates = models.JSONField(
        default=list,
        verbose_name=_("Booking Dates"),
        help_text=_("List of dates when the room is booked"),
    )

    # Location
    floor_number = models.PositiveIntegerField(verbose_name=_("Floor Number"))
    view = models.CharField(
        max_length=100,
        verbose_name=_("View"),
        help_text=_("Description of the room's view"),
    )
    proximity_to_facilities = models.JSONField(
        default=dict,
        verbose_name=_("Proximity to Facilities"),
        help_text=_("Distance to key hotel facilities"),
    )

    # Room Features
    size = models.CharField(max_length=50, verbose_name=_("Room Size"))

    class SmokingPolicy(models.TextChoices):
        SMOKING = "SMOKING", _("Smoking")
        NON_SMOKING = "NON_SMOKING", _("Non-Smoking")

    smoking_policy = models.CharField(
        max_length=20,
        choices=SmokingPolicy.choices,
        default=SmokingPolicy.NON_SMOKING,
        verbose_name=_("Smoking Policy"),
    )
    accessibility_features = models.TextField(
        blank=True, null=True, verbose_name=_("Accessibility Features")
    )

    # Metadata
    creation_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Creation Date")
    )
    last_updated = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated"))

    def __str__(self):
        return f"{self.room_id}"

    def get_product_code(self):
        return f"{self.hotel.hotel_name}_{self.room_id}"


class Reservation(models.Model):
    # Reservation Identification
    reservation_id = models.AutoField(
        unique=True, primary_key=True, verbose_name=_("Reservation ID")
    )
    booking_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Booking Date")
    )

    # User Information
    user = models.ForeignKey(
        accounts.models.CustomUser,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name=_("User"),
    )

    special_requests = models.TextField(
        blank=True, null=True, verbose_name=_("Special Requests")
    )

    # Room and Hotel Information
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name=_("Room"),
    )
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name=_("Hotel"),
    )

    # Booking Dates
    check_in_date = models.DateField(verbose_name=_("Check-in Date"))
    check_out_date = models.DateField(verbose_name=_("Check-out Date"))

    # Payment Information
    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        PAID = "PAID", _("Paid")
        CANCELLED = "CANCELLED", _("Cancelled")
        REFUNDED = "REFUNDED", _("Refunded")

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name=_("Payment Status"),
    )
    payment_ref_id = models.ForeignKey(
        PaymentHistory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Payment Reference"),
    )

    # Additional Details
    number_of_guests = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], verbose_name=_("Number of Guests")
    )
    is_checked_in = models.BooleanField(default=False, verbose_name=_("Is Checked In"))
    is_checked_out = models.BooleanField(
        default=False, verbose_name=_("Is Checked Out")
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")
        ordering = ["-booking_date"]
        indexes = [
            models.Index(fields=["reservation_id"]),
            models.Index(fields=["check_in_date", "check_out_date"]),
        ]

    def __str__(self):
        return f"Reservation {self.reservation_id} by {self.user.get_full_name()}"

    def calculate_total_nights(self):
        """Calculate the total number of nights for the reservation."""
        return (self.check_out_date - self.check_in_date).days

    def calculate_total_amount(self):
        """Calculate the total amount based on room price and number of nights."""
        nights = self.calculate_total_nights()
        return nights * self.room.base_price

    def is_active(self):
        """Check if the reservation is currently active."""
        today = timezone.now().date()
        return self.check_in_date <= today <= self.check_out_date

    def save(self, *args, **kwargs):
        """Override save method to ensure data consistency."""
        if self.check_out_date <= self.check_in_date:
            raise ValidationError(_("Check-out date must be after check-in date"))
        if int(self.number_of_guests) > int(self.room.max_occupancy):
            raise ValidationError(_("Number of guests exceeds room capacity"))
        super().save(*args, **kwargs)


class HotelImage(models.Model):
    class Meta:
        verbose_name = _("Hotel Image")
        verbose_name_plural = _("Hotel Images")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["hotel", "created_at"]),
        ]
        # Add constraint to ensure only one primary image per hotel
        constraints = [
            models.UniqueConstraint(
                fields=["hotel"],
                condition=models.Q(is_primary=True),
                name="unique_primary_image_per_hotel",
            )
        ]

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Hotel"),
        help_text=_("The hotel this image belongs to"),
    )
    image = models.ImageField(
        upload_to="images/hotels/%Y/%m/%d/",
        verbose_name=_("Image"),
        help_text=_("Upload a high-quality image of the hotel"),
    )
    caption = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Caption"),
        help_text=_("Optional description of the image"),
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name=_("Primary Image"),
        help_text=_("Mark as the main display image for the hotel"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    def __str__(self):
        return f"Image {self.id} for {self.hotel.hotel_name}"

    def save(self, *args, **kwargs):
        """Ensure only one primary image per hotel"""
        if self.is_primary:
            HotelImage.objects.filter(hotel=self.hotel, is_primary=True).exclude(
                pk=self.pk
            ).update(is_primary=False)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.is_primary:
            new_primary = (
                HotelImage.objects.filter(hotel=self.hotel).exclude(pk=self.pk).first()
            )
            if new_primary:
                new_primary.is_primary = True
                new_primary.save()
        super().delete(*args, **kwargs)


class RoomImage(models.Model):
    class Meta:
        verbose_name = _("Room Image")
        verbose_name_plural = _("Room Images")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["room", "created_at"]),
        ]

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Room"),
        help_text=_("The room this image belongs to"),
    )
    image = models.ImageField(
        upload_to="images/rooms/%Y/%m/%d/",
        verbose_name=_("Image"),
        help_text=_("Upload a high-quality image of the room"),
    )
    caption = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Caption"),
        help_text=_("Optional description of the image"),
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name=_("Primary Image"),
        help_text=_("Mark as the main display image for the room"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    def __str__(self):
        return f"Image {self.id} for Room {self.room.room_name} in {self.room.hotel.hotel_name}"

    def save(self, *args, **kwargs):
        """Ensure only one primary image per room"""
        if self.is_primary:
            RoomImage.objects.filter(room=self.room, is_primary=True).update(
                is_primary=False
            )
        super().save(*args, **kwargs)
