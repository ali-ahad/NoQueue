from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.contrib.auth.models import User
from .models import OwnerProfile
from .models import CustomerProfile, Transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput, DateInput
from django.forms import ModelForm
from django.contrib.admin import widgets 
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget

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

"""class DateTimePicker(forms.Form):

	datetime = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M:%S'], widget=forms.DateTimeInput(format='%d/%m/%Y %H:%M:%S'))
	def clean(self):
		cleaned_data = self.cleaned_data
		return cleaned_data"""

"""class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )"""

"""class ProjectForm(ModelForm):
	startdate = forms.DateField()
	starthour = forms.ChoiceField(choices=((6,"6am"),(7,"7am"),(8,"8am"),(9,"9am")))
	startminute = forms.ChoiceField(choices=((0,":00"),(15,":15"),(30,":30"),(45,":45")))

	class Meta:
		model = ProjectForm
	
	def __init__(self, *args, **kwargs):
		super(ProjectForm, self).__init__(*args, **kwargs)
		self.fields['startdate'].widget = widgets.AdminDateWidget()
		self.fields['starthour'].widget = widgets.AdminTimeWidget()
		self.fields['startminute'].widget = widgets.AdminSplitDateTime()

	def clean(self):
		starttime = time(int(self.cleaned_data.get('starthour')), 
								int(self.cleaned_data.get('startminute')))
		return self.cleaned_data"""

"""class DateTime(forms.ModelForm):
	class Meta:
		#model = yourModel
		widgets = {
			#Use localization and bootstrap 3
			'datetime': DateTimeWidget(attrs={'id':"yourdatetimeid"}, usel10n = True, bootstrap_version=3)
		}"""


        
class PreForm(forms.Form):
	year = forms.CharField(max_length=4, min_length=4, widget=TextInput(attrs={'placeholder': 'Enter Year'}))
	month = forms.CharField(max_length=2, min_length=1, widget=TextInput(attrs={'placeholder': 'Enter Month'}))
	day = forms.CharField(max_length=2, min_length=1, widget=TextInput(attrs={'placeholder': 'Enter Day'}))
	hour = forms.CharField(max_length=2, min_length=2, widget=TextInput(attrs={'placeholder': 'Enter Hour'}))
	min = forms.CharField(max_length=2, min_length=2, widget=TextInput(attrs={'placeholder': 'Enter Min'}))
