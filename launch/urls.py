from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "launch"

urlpatterns = [
    path('', views.home, name='launch-home'),
    path('restaurant-launch/', views.restaurant_launch, name='launch-restaurant'),
    path('customer-launch/', views.customer_launch, name='launch-customer'),
    path('restaurant-register/', views.register_restaurant, name='launch-restaurant-register'),
    path('restaurant-login/', auth_views.LoginView.as_view(template_name='launch/restaurant-login.html'), name='launch-restaurant-login'),
    path('customer-register/', views.register_customer, name='launch-customer-register'),
    path('customer-login/', auth_views.LoginView.as_view(template_name='launch/customer-login.html'), name='launch-customer-login'),
]

