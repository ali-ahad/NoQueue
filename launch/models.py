from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    is_owner = models.BooleanField(default= True)

class OwnerProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='owner_profile')
	bio = models.CharField(max_length=30, blank=True)
	location = models.CharField(max_length=30, blank=True)
  
class CustomerProfile(models.Model):
  	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='customer_profile')
  	company_name = models.CharField(max_length=100, blank=True)
  	website = models.CharField(max_length=100, blank=True)
	
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
	# print(instance.internprofile.bio, instance.internprofile.location)
	if instance.is_owner:
		instance.owner_profile.save()
	else:
		CustomerProfile.objects.get_or_create(user = instance)
	