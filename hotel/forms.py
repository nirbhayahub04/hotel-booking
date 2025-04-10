from django import forms
from django.utils.translation import gettext_lazy as _

from hotel.models import Hotel, Room

COMMON_INPUT_CLASSES = (
    "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm "
    "ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 "
    "focus:ring-2 focus:ring-inset focus:ring-amber-600 sm:text-sm sm:leading-6"
)

TEXTAREA_CLASSES = (
    "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm "
    "ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 "
    "focus:ring-2 focus:ring-inset focus:ring-amber-600 sm:text-sm sm:leading-6"
)


class BasicInformationForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = [
            "hotel_name",
            "description",
            "phone_number",
            "email",
            "website",
            "star_rating",
        ]
        widgets = {
            "hotel_name": forms.TextInput(
                attrs={
                    "class": COMMON_INPUT_CLASSES,
                    "placeholder": _("Yak & Yeti Hotel"),
                    "autocomplete": "organization",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASSES,
                    "rows": 3,
                    "placeholder": _(
                        "A luxurious 5-star hotel in the heart of Kathmandu"
                    ),
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": COMMON_INPUT_CLASSES,
                    "placeholder": _("+977 1-4248999"),
                    "autocomplete": "tel",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": COMMON_INPUT_CLASSES,
                    "placeholder": _("info@yakandyeti.com.np"),
                    "autocomplete": "email",
                }
            ),
            "website": forms.URLInput(
                attrs={
                    "class": COMMON_INPUT_CLASSES,
                    "placeholder": _("https://www.yakandyeti.com.np"),
                    "autocomplete": "url",
                }
            ),
            "star_rating": forms.NumberInput(
                attrs={"class": COMMON_INPUT_CLASSES, "min": "1", "max": "5"}
            ),
        }
        help_texts = {
            "star_rating": _("Official star rating (1-5 stars)"),
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = [
            "address",
            "city",
            "state",
            "country",
            "postal_code",
            "latitude",
            "longitude",
        ]
        widgets = {
            "address": forms.TextInput(
                attrs={
                    "class": COMMON_INPUT_CLASSES,
                    "placeholder": _("Durbar Marg"),
                    "autocomplete": "street-address",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": COMMON_INPUT_CLASSES,
                    "placeholder": _("Kathmandu"),
                    "autocomplete": "address-level2",
                }
            ),
            "state": forms.TextInput(
                attrs={
                    "class": COMMON_INPUT_CLASSES,
                    "placeholder": _("Bagmati"),
                    "autocomplete": "address-level1",
                }
            ),
            "country": forms.TextInput(
                attrs={
                    "class": COMMON_INPUT_CLASSES,
                    "placeholder": _("Nepal"),
                    "autocomplete": "country",
                }
            ),
            "postal_code": forms.TextInput(
                attrs={
                    "class": COMMON_INPUT_CLASSES,
                    "placeholder": _("44600"),
                    "autocomplete": "postal-code",
                }
            ),
            "latitude": forms.NumberInput(
                attrs={
                    "class": COMMON_INPUT_CLASSES,
                    "step": "0.000001",
                    "placeholder": _("27.7136"),
                }
            ),
            "longitude": forms.NumberInput(
                attrs={
                    "class": COMMON_INPUT_CLASSES,
                    "step": "0.000001",
                    "placeholder": _("85.3158"),
                }
            ),
        }


class AmenitiesForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ["amenities"]
        widgets = {
            "amenities": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASSES,
                    "rows": 4,
                    "placeholder": _("Pool, Gym, Spa, Free WiFi, Restaurant"),
                }
            ),
        }
        help_texts = {
            "amenities": _("List of available amenities (comma-separated)"),
        }


class PoliciesForm(forms.Form):
    check_in_time = forms.TimeField(
        widget=forms.TimeInput(attrs={"class": COMMON_INPUT_CLASSES, "type": "time"}),
        initial="15:00",
        help_text=_("Standard check-in time"),
    )
    check_out_time = forms.TimeField(
        widget=forms.TimeInput(attrs={"class": COMMON_INPUT_CLASSES, "type": "time"}),
        initial="11:00",
        help_text=_("Standard check-out time"),
    )


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]

        if initial:
            if not isinstance(initial, list):
                initial = [initial]
            result = initial + result

        print("Clean Form", result)
        return result


class HotelImageForm(forms.Form):
    images = MultipleFileField(
        widget=MultipleFileInput(
            attrs={
                "type": "file",
                "name": "images",
                "accept": "image/*",
                "multiple": "multiple",
                "class": "block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-amber-50 file:text-amber-700 hover:file:bg-amber-100",
            }
        ),
        label="Hotel Images",
    )


class RoomImageForm(forms.Form):
    images = MultipleFileField(
        widget=MultipleFileInput(
            attrs={
                "type": "file",
                "name": "images",
                "accept": "image/*",
                "multiple": "multiple",
                "class": "block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-amber-50 file:text-amber-700 hover:file:bg-amber-100",
            }
        ),
        label="Room Images",
    )
