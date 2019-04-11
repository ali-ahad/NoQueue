from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
import datetime


# Class that sees whether the user is owner or customer
class User(AbstractUser):
    is_owner = models.BooleanField(default= True)

# Class for dealing with restaurant owner
class OwnerProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='owner_profile')
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')

	def __str__(self):
		return self.user.username

	
class Item(models.Model):
	name = models.CharField(max_length=100)
	price = models.DecimalField(max_digits=6,decimal_places=2, default =0.00)
	description = models.CharField(max_length=60)
	restaurant = models.ForeignKey('Restaurant', on_delete = models.CASCADE) #gets user from user tables. 
	image = models.ImageField(default='rest_default.jpg', upload_to='restaurant_pics')

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('launch:restaurant-menu', kwargs={'pk':self.restaurant.pk})


# Class for dealing with customer
class CustomerProfile(models.Model):
  	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='customer_profile')
  	image = models.ImageField(default='default.jpg', upload_to='profile_pics')
  	cart = models.ManyToManyField(Item, blank = True)

  	def __str__ (self):
  		return self.user.username



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




# Class for dealing with restaurants
class Restaurant(models.Model):
	name = models.CharField(max_length=100)
	location = models.CharField(max_length=300)
	cuisine = models.CharField(max_length=50)
	description = models.CharField(max_length=400)
	owner = models.ForeignKey(OwnerProfile, on_delete = models.CASCADE) #gets user from user tables.
	image = models.ImageField(default='rest_default.jpg', upload_to='restaurant_pics')

	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('launch:launch-home')
	
	

class OrderItem(models.Model):
    product = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default = 1)
    is_ordered = models.BooleanField(default=False)

    
    def __str__(self):
        return self.product.name



class Order(models.Model):
    ref_code = models.CharField(max_length=15)
    owner = models.ForeignKey(CustomerProfile, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
    	sum = 0
    	for item in self.items.all():
    		sum = sum + (int(item.product.price) * int(item.quantity))
    	return sum

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.ref_code)

class Transaction(models.Model):
	profile = models.ForeignKey(CustomerProfile, on_delete = models.CASCADE)
	order = models.ForeignKey(Order, on_delete = models.CASCADE,default=0)
	restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE, default='')
	orderStatus = models.CharField(max_length=10, default="Pending")
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	collect_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, default=datetime.datetime.now)
	owner = models.ForeignKey(OwnerProfile, on_delete = models.CASCADE, default = 0)
	isTransacted = models.BooleanField(default=False)
	price = models.IntegerField(default = 0)

	def get_order_total(self):
		sum = 0
		for item in self.order.items.all():
			sum = sum + (int(item.product.price) * int(item.quantity))
		return sum
	
	def get_order_items(self):
		return self.order.items.all()

	def get_restaurant_id(self):
		return self.restaurant.pk

	def get_order_id(self):
		return self.order.ref_code

	def get_Customer_id(self):
		return self.profile.pk

	def accept(self):
		print("lmao")
		self.orderStatus = 'Accepted'
		self.save()

	def reject(self):
		print("lolerz")
		self.orderStatus = 'Rejected'
		self.save()
	class Meta:
		ordering = ['-timestamp']	



