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



class UserForm(UserCreationForm):
	first_name = forms.CharField()
	last_name = forms.CharField()
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

class OwnerProfileForm(forms.ModelForm):
	images = forms.ImageField()
	class Meta:
		model = OwnerProfile
		fields = ('location', 'bio', 'images')
        
class CustomerProfileForm(forms.ModelForm):
	images = forms.ImageField()
	class Meta:
		model = CustomerProfile
		fields = ('company_name', 'website', 'images')

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['email']

class CustomerUpdateForm(forms.ModelForm):
	class Meta:
		model = CustomerProfile
		fields = ('company_name', 'website', 'image')
class OwnerUpdateForm(forms.ModelForm):
	class Meta:
		model = OwnerProfile
		fields = ('location', 'bio', 'image')
        
