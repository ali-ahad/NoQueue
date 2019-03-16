from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterUser
      
def home(request):
   return render(request, 'launch/launch.html')

def register(request):
   if request.method == 'POST':
      form = RegisterUser(request.POST)
      if form.is_valid():
         form.save()
         username = form.cleaned_data.get('username')
         messages.success(request, f'Account created for {username}!')
         return redirect('launch:launch-login')
   else:
      form = RegisterUser()
   return render(request, 'launch/register.html', {'form': form})
