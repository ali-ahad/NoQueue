from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterUser
      
def home(request):
   return render(request, 'launch/launch.html')

def restaurant_launch(request):
   return render(request, 'launch/restaurant-launch.html')

def customer_launch(request):
   return render(request, 'launch/customer-launch.html')

def register_restaurant(request):
   if request.method == 'POST':
      form = RegisterUser(request.POST)
      if form.is_valid():
         form.save()
         username = form.cleaned_data.get('username')
         messages.success(request, f'Account created for {username}!')
         return redirect('launch:launch-restaurant-login')
   else:
      form = RegisterUser()
   return render(request, 'launch/restaurant-register.html', {'form': form})

def register_customer(request):
   if request.method == 'POST':
      form = RegisterUser(request.POST)
      if form.is_valid():
         form.save()
         username = form.cleaned_data.get('username')
         messages.success(request, f'Account created for {username}!')
         return redirect('launch:launch-customer-login')
   else:
      form = RegisterUser()
   return render(request, 'launch/customer-register.html', {'form': form})
