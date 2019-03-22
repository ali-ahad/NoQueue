from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import RestaurantDetailView, RestaurantCreateView

app_name = "launch"

urlpatterns = [

    # Initial page when app launches
    path('', views.home, name='launch-home'),

    # Page that loads when the user registers
    path('register/', views.register, name='register'),

    # Page that aks how to register. As a customer or register
    path('register-owner/', views.register_owner, name='register-owner'),
    path('register-customer/', views.register_customer, name='register-customer'),

    # Page that asks how to launch the page when logged in. As a customer or register
    path('owner-register/', views.owner_profile_view, name='launch-register-owner'),
    path('customer-register/', views.customer_profile_view, name='launch-register-customer'),
    
    # Paths to redirect towards log in and log out pages
    path('login/', auth_views.LoginView.as_view(template_name='launch/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='launch/logout.html'), name='logout'),

    # Path that shows the profile for customers or owner
    path('profile/', views.show_profile, name='profile'),

    #shows detail of restuarant using class based views
    path('restaurant/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'), 

    #creates restuarant using class based views
    path('restaurant/new/', RestaurantCreateView.as_view(), name='restaurant-create')


]	
