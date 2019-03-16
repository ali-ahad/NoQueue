from django.urls import path
from . import views

app_name = "launch"

urlpatterns = [
    path('', views.home, name='launch-home'),
    path('register/', views.register, name='launch-register'),
]

