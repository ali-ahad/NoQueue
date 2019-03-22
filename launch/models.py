from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

# Class that sees whether the user is owner or customer
class User(AbstractUser):
    is_owner = models.BooleanField(default= True)

# Class for dealing with restaurant owner
class OwnerProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='owner_profile')
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')

	def __str__(self):
		return self.user.username
  
# Class for dealing with customer
class CustomerProfile(models.Model):
  	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='customer_profile')
  	image = models.ImageField(default='default.jpg', upload_to='profile_pics')

  	def __str__ (self):
  		return self.user.username

# Class for dealing with restaurants
class Restaurant(models.Model):
	name = models.CharField(max_length=100)
	location = models.CharField(max_length=300)
	cuisine = models.CharField(max_length=50)
	owner = models.ForeignKey(User, on_delete = models.CASCADE) #gets user from user tables. 
	image = models.ImageField(default='rest_default.jpg', upload_to='restaurant_pics')

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('launch:restaurant-detail', kwargs={'pk':self.pk})
	
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	print('****', created)
	if instance.is_owner:
		OwnerProfile.objects.get_or_create(user = instance)

	else:
		CustomerProfile.objects.get_or_create(user = instance)
	
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	print('_-----')	
	if instance.is_owner:
		instance.owner_profile.save()

	else:
		CustomerProfile.objects.get_or_create(user = instance)



