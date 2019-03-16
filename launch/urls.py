from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "launch"

urlpatterns = [
    path('', views.home, name='launch-home'),
    path('register/', views.register, name='launch-register'),
    path('login/', auth_views.LoginView.as_view(template_name='launch/login.html'), name='launch-login'),
]

