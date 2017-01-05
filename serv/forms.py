from django import forms
from django.core.validators import RegexValidator
from phonenumber_field.formfields import PhoneNumberField

class KeyRequestForm(forms.Form): pass

class LoginForm(forms.Form):
	username = forms.CharField(label="Username", max_length=64, required=True)
	password = forms.CharField(label="Password", max_length=64, required=True,
							   widget=forms.PasswordInput)

class UserRequestForm(forms.Form):
	organization_name = forms.CharField(label="Organization Name",
										max_length=64, required=True)
	contact_name = forms.CharField(label="Contact Name", max_length=64, required=True)
	contact_email = forms.CharField(label="Email", max_length=64, required=True,
							        widget=forms.EmailInput)

	contact_phone = PhoneNumberField(label="Phone", required=False)
	username = forms.CharField(label="Username", max_length=64, required=True)
	
	password = forms.CharField(label="Password", max_length=64, required=True,
							   widget=forms.PasswordInput)

	password_repeat = forms.CharField(label="Password", max_length=64, required=True,
									  widget=forms.PasswordInput)

class ToggleActiveUserForm(forms.Form):
	username = forms.CharField(label="Username", max_length=64, required=True, 
							   widget=forms.HiddenInput())
