from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import OwnerProfile
from .models import CustomerProfile
from .models import Restaurant

admin.site.register(User, UserAdmin)
admin.site.register(OwnerProfile)
admin.site.register(CustomerProfile)
admin.site.register(Restaurant)