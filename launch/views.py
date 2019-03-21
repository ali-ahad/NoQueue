from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm
from .forms import OwnerProfileForm
from .forms import CustomerProfileForm  

def home(request):
   if request.user.is_authenticated:
      if request.user.is_owner:
         return render(request, 'launch/launch.html')
      else:
         return render(request, 'launch/launch.html')

   else:   
      return render(request, 'launch/launch.html')

def register(request):
   return render(request, 'launch/register.html')

def register_owner(request):
   return render(request, 'launch/register-owner.html')

def register_customer(request):
   return render(request, 'launch/register-customer.html')


def owner_profile_view(request):
   if request.method == 'POST':
      user_form = UserForm(request.POST, prefix='UF')
      profile_form = OwnerProfileForm(request.POST, prefix='PF')

      
      if user_form.is_valid() and profile_form.is_valid():
         user = user_form.save(commit=False)
         user.save()
         username = user.username
         user.owner_profile.bio = profile_form.cleaned_data.get('bio')
         user.owner_profile.location = profile_form.cleaned_data.get('location')
         user.owner_profile.save()
         messages.success(request, f'Account created for {username}!')
         return redirect('launch:launch-home')
      
         
   else:
      user_form = UserForm(prefix='UF')
      profile_form = OwnerProfileForm(prefix='PF')
      
   return render(request, 'launch/register-owner.html',{
         'user_form': user_form,
         'profile_form': profile_form,
      })

def customer_profile_view(request):
   if request.method == 'POST':
      user_form = UserForm(request.POST, prefix='UF')
      profile_form = CustomerProfileForm(request.POST, prefix='PF')

      if user_form.is_valid() and profile_form.is_valid():
         user = user_form.save(commit=False)
         user.is_owner = False
         user.save()
         user.customer_profile.company_name = profile_form.cleaned_data.get('company_name')
         user.customer_profile.website = profile_form.cleaned_data.get('website')
         user.customer_profile.save()

         username = user.username
         messages.success(request, f'Account created for {username}!')
         return redirect('launch:launch-home')
         
   else:
      user_form = UserForm(prefix='UF')
      profile_form = CustomerProfileForm(prefix='PF')
      
   return render(request, 'launch/register-customer.html',{
         'user_form': user_form,
         'profile_form': profile_form,
      })