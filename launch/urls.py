from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "launch"

urlpatterns = [
    path('', views.home, name='launch-home'),

    path('register/', views.register, name='register'),
    path('register-owner/', views.register_owner, name='register-owner'),
    path('register-customer/', views.register_customer, name='register-customer'),


    path('owner-register/', views.owner_profile_view, name='launch-register-owner'),
    path('customer-register/', views.customer_profile_view, name='launch-register-customer'),
    


    path('login/', auth_views.LoginView.as_view(template_name='launch/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='launch/logout.html'), name='logout')
]

