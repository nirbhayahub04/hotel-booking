from django import forms
from django.utils.translation import gettext_lazy as _
from hotel.models import Hotel, Room

COMMON_INPUT_CLASSES = "w-full px-3 py-2 border rounded-md"
TEXTAREA_CLASSES = "w-full px-3 py-2 border rounded-md"


class HotelUpdateForm(forms.ModelForm):
    class Meta:
        model = Hotel
        exclude = ("hotel_id", "creation_date", "last_updated")
        widgets = {
            "hotel_name": forms.TextInput(
                attrs={"class": COMMON_INPUT_CLASSES, "autocomplete": "organization"}
            ),
            "address": forms.TextInput(
                attrs={"class": COMMON_INPUT_CLASSES, "autocomplete": "street-address"}
            ),
            "description": forms.Textarea(attrs={"class": TEXTAREA_CLASSES, "rows": 3}),
            "amenities": forms.Textarea(attrs={"class": TEXTAREA_CLASSES, "rows": 3}),
            "phone_number": forms.TextInput(
                attrs={"class": COMMON_INPUT_CLASSES, "autocomplete": "tel"}
            ),
            "email": forms.EmailInput(
                attrs={"class": COMMON_INPUT_CLASSES, "autocomplete": "email"}
            ),
            "website": forms.URLInput(
                attrs={"class": COMMON_INPUT_CLASSES, "autocomplete": "url"}
            ),
            "star_rating": forms.NumberInput(attrs={"class": COMMON_INPUT_CLASSES}),
        }


class RoomForm(forms.ModelForm):
    seasonal_pricing = forms.JSONField(
        widget=forms.Textarea(
            attrs={
                "class": TEXTAREA_CLASSES,
                "rows": 2,
                "placeholder": _('{"peak": 250, "off_peak": 180}'),
            }
        ),
        required=False,
    )

    additional_fees = forms.JSONField(
        widget=forms.Textarea(
            attrs={
                "class": TEXTAREA_CLASSES,
                "rows": 2,
                "placeholder": _('{"extra_guest": 50, "late_checkout": 20}'),
            }
        ),
        required=False,
    )

    booking_dates = forms.JSONField(
        widget=forms.Textarea(
            attrs={
                "class": TEXTAREA_CLASSES,
                "rows": 2,
                "placeholder": _('["2023-12-25", "2024-01-01"]'),
            }
        ),
        required=False,
    )

    proximity_to_facilities = forms.JSONField(
        widget=forms.Textarea(
            attrs={
                "class": TEXTAREA_CLASSES,
                "rows": 2,
                "placeholder": _('{"elevator": "10m", "pool": "20m"}'),
            }
        ),
        required=False,
    )

    class Meta:
        model = Room
        fields = [
            "room_id",
            "room_type",
            "bed_configuration",
            "max_occupancy",
            "amenities",
            "bathroom_type",
            "base_price",
            "floor_number",
            "view",
            "proximity_to_facilities",
            "size",
            "smoking_policy",
            "accessibility_features",
        ]
        widgets = {
            "room_id": forms.TextInput(
                attrs={"class": COMMON_INPUT_CLASSES, "placeholder": _("Room ID")}
            ),
            "room_type": forms.Select(attrs={"class": COMMON_INPUT_CLASSES}),
            "bed_configuration": forms.TextInput(
                attrs={
                    "class": COMMON_INPUT_CLASSES,
                    "placeholder": _("1 King Bed, 2 Queen Beds"),
                }
            ),
            "max_occupancy": forms.NumberInput(
                attrs={"class": COMMON_INPUT_CLASSES, "placeholder": _("4")}
            ),
            "amenities": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASSES,
                    "rows": 3,
                    "placeholder": _("Wi-Fi, TV, Minibar, Air Conditioning"),
                }
            ),
            "bathroom_type": forms.TextInput(
                attrs={
                    "class": COMMON_INPUT_CLASSES,
                    "placeholder": _("Private with shower"),
                }
            ),
            "base_price": forms.NumberInput(
                attrs={"class": COMMON_INPUT_CLASSES, "placeholder": _("200.00")}
            ),
            "floor_number": forms.NumberInput(
                attrs={"class": COMMON_INPUT_CLASSES, "placeholder": _("5")}
            ),
            "view": forms.TextInput(
                attrs={"class": COMMON_INPUT_CLASSES, "placeholder": _("Ocean View")}
            ),
            "size": forms.TextInput(
                attrs={"class": COMMON_INPUT_CLASSES, "placeholder": _("50 sqm")}
            ),
            "smoking_policy": forms.Select(attrs={"class": COMMON_INPUT_CLASSES}),
            "accessibility_features": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASSES,
                    "rows": 3,
                    "placeholder": _("Wheelchair access, grab bars"),
                }
            ),
        }
