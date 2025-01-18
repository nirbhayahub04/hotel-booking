from django import forms

from hotel.models import HotelModel, RoomModel


class HotelForm( forms.ModelForm ):
	class Meta:
		model = HotelModel
		fields = '__all__'


class HotelUpdateForm( HotelForm ):
	class Meta:
		model = HotelModel
		fields = '__all__'
		exclude = ('id', 'created_at', 'updated_at')
		widgets = {
			'name': forms.TextInput(
				attrs={
					'class': 'form-control'
				}
			),
			'address': forms.TextInput(
				attrs={
					'class': 'form-control'
				}
			)
		}
		labels = {
			'name': 'Name',
			'address': 'Address'
		}
		help_texts = {
			'name': 'Enter Hotel Name',
			'address': 'Enter Hotel Address'
		}
		error_messages = {
			'name': {
				'required': 'Name is required'
			},
			'address': {
				'required': 'Address is required'
			}
		}
		required = {
			'name': True,
			'address': True
		}


class RoomForm( forms.ModelForm ):
	room_number = forms.CharField(
		required=True,
		widget=forms.TextInput(
			attrs={
				"placeholder": "Room Number",
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
                            focus:ring-indigo-600 sm:text-sm sm:leading-6"
			}
		)
	)
	room_type = forms.CharField(
		required=True,
		widget=forms.TextInput(
			attrs={
				"placeholder": "Room Type",
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
				"
			}
		)
	)
	price = forms.CharField(
		required=True,
		widget=forms.TextInput(
			attrs={
				"placeholder": "Price",
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
				"
			}
		)
	)
	image = forms.ImageField(
		required=False,
		widget=forms.FileInput(
			attrs={
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
                            focus:ring-indigo-600 sm:text-sm sm:leading-6"
			}
		)
	)
	capacity = forms.IntegerField(
		required=True,
		widget=forms.TextInput(
			attrs={
				"placeholder": "Capacity",
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
                            focus:ring-indigo-600 sm:text-sm sm:leading-6"
			}
		)
	)


	class Meta:
		model = RoomModel
		fields = [
			'room_number',
			'room_type',
			'price',
			'image',
			'capacity'
		]
