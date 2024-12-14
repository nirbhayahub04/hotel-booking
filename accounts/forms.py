from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class LoginForm( forms.Form ):
	username = forms.CharField(
		required = True,
		widget = forms.TextInput(
			attrs = {
				"placeholder": "Username",
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
                            focus:ring-indigo-600 sm:text-sm sm:leading-6"
			}
		)
	)

	password = forms.CharField(
		required = True,
		widget = forms.PasswordInput(
			attrs = {
				"placeholder": "Password",
				"class": "block w-full rounded-md border-0 \
                        py-1.5 text-gray-900 shadow-sm ring-1 \
                        ring-inset ring-gray-300 \
                        placeholder:text-gray-400 \
                        focus:ring-2 focus:ring-inset \
                        focus:ring-indigo-600 \
                        sm:text-sm sm:leading-6"
			}
		)
	)


class UserSignUpForm( UserCreationForm ):
	first_name = forms.CharField(
		required = True,
		widget = forms.TextInput(
			attrs = {
				"placeholder": "First Name",
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
                            focus:ring-indigo-600 sm:text-sm sm:leading-6"
			}
		)
	)
	last_name = forms.CharField(
		required = True,
		widget = forms.TextInput(
			attrs = {
				"placeholder": "Last Name",
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
                            focus:ring-indigo-600 sm:text-sm sm:leading-6"
			}
		)
	)
	email = forms.EmailField(
		required = True,
		widget = forms.EmailInput(
			attrs = {
				"placeholder": "Email",
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
                            focus:ring-indigo-600 sm:text-sm sm:leading-6"
			}
		)
	)
	phone_number = forms.CharField(
		required = True,
		widget = forms.TextInput(
			attrs = {
				"placeholder": "Phone Number",
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
                            focus:ring-indigo-600 sm:text-sm sm:leading-6"
			}
		)
	)
	username = forms.CharField(
		required = True,
		widget = forms.TextInput(
			attrs = {
				"placeholder": "Username",
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
                            focus:ring-indigo-600 sm:text-sm sm:leading-6"
			}
		)
	)
	address = forms.CharField(
		required = False,
		widget = forms.TextInput(
			attrs = {
				"placeholder": "Address",
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
                            focus:ring-indigo-600 sm:text-sm sm:leading-6"
			}
		)
	)
	password1 = forms.CharField(
		required = True,
		widget = forms.PasswordInput(
			attrs = {
				"placeholder": "Password",
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
                            focus:ring-indigo-600 sm:text-sm sm:leading-6"
			}
		)
	)
	password2 = forms.CharField(
		required = True,
		widget = forms.PasswordInput(
			attrs = {
				"placeholder": "Confirm Password",
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
                            focus:ring-indigo-600 sm:text-sm sm:leading-6"
			}
		)
	)

	role = 'customer'

	class Meta:
		model = CustomUser
		fields = ('first_name', 'last_name', 'address', 'username',
		          'email', 'phone_number', 'password1', 'password2',
		          'role')


class ClientSignUpForm( UserCreationForm ):
	first_name = forms.CharField(
		required = True,
		widget = forms.TextInput(
			attrs = {
				"placeholder": "First Name",
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
                            focus:ring-indigo-600 sm:text-sm sm:leading-6"
			}
		)
	)
	last_name = forms.CharField(
		required = True,
		widget = forms.TextInput(
			attrs = {
				"placeholder": "Last Name",
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
                            focus:ring-indigo-600 sm:text-sm sm:leading-6"
			}
		)
	)
	email = forms.EmailField(
		required = True,
		widget = forms.EmailInput(
			attrs = {
				"placeholder": "Email",
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
                            focus:ring-indigo-600 sm:text-sm sm:leading-6"
			}
		)
	)
	phone_number = forms.CharField(
		required = True,
		widget = forms.TextInput(
			attrs = {
				"placeholder": "Phone Number",
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
                            focus:ring-indigo-600 sm:text-sm sm:leading-6"
			}
		)
	)
	username = forms.CharField(
		required = True,
		widget = forms.TextInput(
			attrs = {
				"placeholder": "Username",
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
                            focus:ring-indigo-600 sm:text-sm sm:leading-6"
			}
		)
	)
	address = forms.CharField(
		required = False,
		widget = forms.TextInput(
			attrs = {
				"placeholder": "Address",
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
                            focus:ring-indigo-600 sm:text-sm sm:leading-6"
			}
		)
	)
	password1 = forms.CharField(
		required = True,
		widget = forms.PasswordInput(
			attrs = {
				"placeholder": "Password",
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
                            focus:ring-indigo-600 sm:text-sm sm:leading-6"
			}
		)
	)
	password2 = forms.CharField(
		required = True,
		widget = forms.PasswordInput(
			attrs = {
				"placeholder": "Confirm Password",
				"class": "ring-1 ring-inset ring-gray-300 \
                            placeholder:text-gray-40block w-full \
                            rounded-md border-0 py-1.5 text-gray-900 \
                            shadow-sm 0 focus:ring-2 focus:ring-inset \
                            focus:ring-indigo-600 sm:text-sm sm:leading-6"
			}
		)
	)

	class Meta:
		model = CustomUser
		fields = ('first_name', 'last_name', 'address', 'username',
		          'email', 'phone_number', 'password1', 'password2',
		          )
