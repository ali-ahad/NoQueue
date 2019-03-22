from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
	RestaurantDetailView, 
	RestaurantCreateView, 
	RestaurantUpdateView,
	RestaurantDeleteView
	)

app_name = "launch"

urlpatterns = [
    path('', views.home, name='launch-home'),

    path('register/', views.register, name='register'),
    path('register-owner/', views.register_owner, name='register-owner'),
    path('register-customer/', views.register_customer, name='register-customer'),


    path('owner-register/', views.owner_profile_view, name='launch-register-owner'),
    path('customer-register/', views.customer_profile_view, name='launch-register-customer'),
    


    path('login/', auth_views.LoginView.as_view(template_name='launch/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='launch/logout.html'), name='logout'),
    path('profile/', views.show_profile, name='profile'),
    
    #shows detail of restuarant using class based views
    #creates restuarant using class based views
    path('restaurant/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'), 
    path('restaurant/new/', RestaurantCreateView.as_view(), name='restaurant-create'),
    path('restaurant/<int:pk>/update/', RestaurantUpdateView.as_view(), name='restaurant-update'),
    path('restaurant/<int:pk>/delete/', RestaurantDeleteView.as_view(), name='restaurant-delete')



]	
