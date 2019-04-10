from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import OwnerProfile
from .models import CustomerProfile, Order, OrderItem
from .models import Restaurant, Item,Transaction

admin.site.register(User, UserAdmin)
admin.site.register(OwnerProfile)
admin.site.register(CustomerProfile)
admin.site.register(Restaurant)
admin.site.register(Item)
admin.site.register(Transaction)
admin.site.register(Order)
admin.site.register(OrderItem)
