from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.contrib.auth.models import User
from .models import OwnerProfile
from .models import CustomerProfile
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.forms import ModelForm

User = get_user_model()
CHOICES = ['Restaurant Owner', 'Customer']

# Form for registration of a user
class UserForm(UserCreationForm):
	first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter First Name'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter Email'}))
	
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
		widgets = {
        'username': forms.fields.TextInput(attrs={'placeholder': 'Enter Username'}),
		  'password1': forms.fields.TextInput(attrs={'placeholder': 'Enter Password'})  
    	}

	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': "Enter Password"})
		self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': "Repeat Password"})

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Enter Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Enter Password'}))

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

class DateInput(forms.DateInput):
	input_type = 'date'


        
