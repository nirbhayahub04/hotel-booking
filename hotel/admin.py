from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.Hotel)
class HotelModelAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ("hotel_name", "city", "star_rating", "creation_date", "is_active")
    list_filter = ("star_rating", "city", "country", "is_active")
    search_fields = ("hotel_name", "city", "country", "hotel_id")
    ordering = ("hotel_name",)
    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "hotel_id",
                    "hotel_name",
                    "description",
                    "star_rating",
                    "is_active",
                )
            },
        ),
        (
            "Location",
            {
                "fields": (
                    "address",
                    "city",
                    "state",
                    "country",
                    "postal_code",
                    "latitude",
                    "longitude",
                )
            },
        ),
        ("Contact", {"fields": ("phone_number", "email", "website")}),
        (
            "Hotel Features",
            {"fields": ("amenities", "check_in_time", "check_out_time")},
        ),
        ("Metadata", {"fields": ("creation_date", "last_updated")}),
    )


@admin.register(models.Room)
class RoomModelAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = (
        "room_type",
        "base_price",
        "max_occupancy",
        "availability_status",
    )
    list_filter = (
        "room_type",
        "smoking_policy",
        "floor_number",
        "availability_status",
    )
    search_fields = ("room_type", "room_id")
    ordering = ("room_type",)
    fieldsets = (
        (
            "Room Details",
            {
                "fields": (
                    "room_id",
                    "room_type",
                    "base_price",
                    "max_occupancy",
                    "size",
                )
            },
        ),
        (
            "Features",
            {
                "fields": (
                    "amenities",
                    "accessibility_features",
                    "bathroom_type",
                    "view",
                    "proximity_to_facilities",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "maintenance_notes",
                    "availability_status",
                    "last_cleaned_date",
                )
            },
        ),
        (
            "Booking Details",
            {
                "fields": (
                    "check_in_time",
                    "check_out_time",
                    "booking_dates",
                    "guest_information",
                    "special_requests",
                )
            },
        ),
        (
            "Pricing",
            {"fields": ("seasonal_pricing", "additional_fees")},
        ),
        (
            "Metadata",
            {"fields": ("creation_date", "last_updated", "version")},
        ),
    )


@admin.register(models.Reservation)
class ReservationModelAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = (
        "reservation_id",
        "get_guest_email",
        "room",
        "check_in_date",
        "check_out_date",
        "payment_status",
        "is_checked_in",
        "is_checked_out",
    )
    list_filter = (
        "payment_status",
        "check_in_date",
        "check_out_date",
        "is_checked_in",
        "is_checked_out",
    )
    search_fields = ("reservation_id", "guest_email", "room__room_type", "guest_email")
    raw_id_fields = ("room", "user")
    date_hierarchy = "check_in_date"
    ordering = ("-booking_date",)
    fieldsets = (
        (
            "Reservation Details",
            {"fields": ("reservation_id", "user", "room", "hotel")},
        ),
        (
            "Guest Information",
            {
                "fields": (
                    "guest_name",
                    "guest_email",
                    "guest_phone",
                    "special_requests",
                    "number_of_guests",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "check_in_date",
                    "check_out_date",
                    "is_checked_in",
                    "is_checked_out",
                )
            },
        ),
        ("Payment", {"fields": ("total_amount", "payment_status", "payment_method")}),
        ("Metadata", {"fields": ("booking_date", "created_at", "updated_at")}),
    )

    def get_guest_email(self, obj):
        return obj.guest_email
    get_guest_email.short_description = 'Guest Email'
