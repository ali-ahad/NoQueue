from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.contrib.auth.models import User
from .models import OwnerProfile
from .models import CustomerProfile
from django.contrib.auth import get_user_model
User = get_user_model()
CHOICES = ['Restaurant Owner', 'Customer']

# Form for registration of a user
class UserForm(UserCreationForm):
	first_name = forms.CharField()
	last_name = forms.CharField()
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

# Class to append the UserCreationForm for restaurant owner
class OwnerProfileForm(forms.ModelForm):
	images = forms.ImageField()
	class Meta:
		model = OwnerProfile
		fields = ['images']

# Class to append the UserCreationForm for 
class CustomerProfileForm(forms.ModelForm):
	images = forms.ImageField()
	class Meta:
		model = CustomerProfile
		fields = ['images']

# Class to update user form
class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['email']

# Class to update customer information
class CustomerUpdateForm(forms.ModelForm):
	class Meta:
		model = CustomerProfile
		fields = ['image']

# Class to update restaurant owner information
class OwnerUpdateForm(forms.ModelForm):
	class Meta:
		model = OwnerProfile
		fields = ['image']
        
