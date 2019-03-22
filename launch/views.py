from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from .forms import UserForm
from .forms import OwnerProfileForm
from .forms import CustomerProfileForm
from .forms import UserUpdateForm
from .forms import OwnerProfileForm
from .forms import CustomerUpdateForm
from .forms import OwnerUpdateForm

from .models import Restaurant  

def home(request):
   if request.user.is_authenticated:
      username = request.user.username
      if request.user.is_owner:
         context = {

      'restaurants': Restaurant.objects.all(),
      'myrestaurants': Restaurant.objects.filter(owner = request.user.id)
         }

         return render(request, 'launch/launch.html', context)
      else:
         context = {
      'restaurants': Restaurant.objects.all()   }


         return render(request, 'launch/launch.html',context)

   else:   
      context = {
      'restaurants': Restaurant.objects.all()
   }
      return render(request, 'launch/launch.html',context)

def register(request):
   return render(request, 'launch/register.html')

def register_owner(request):
   return render(request, 'launch/register-owner.html')

def register_customer(request):
   return render(request, 'launch/register-customer.html')


def owner_profile_view(request):
   if request.method == 'POST':
      user_form = UserForm(request.POST, prefix='UF')
      profile_form = OwnerProfileForm(request.POST, request.FILES, prefix='PF')

      
      if user_form.is_valid() and profile_form.is_valid():
         user = user_form.save(commit=False)
         user.save()
         username = user.username
         user.owner_profile.bio = profile_form.cleaned_data.get('bio')
         user.owner_profile.location = profile_form.cleaned_data.get('location')
         user.owner_profile.image = profile_form.cleaned_data.get('images')
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
      user_form = UserForm(request.POST)
      profile_form = CustomerProfileForm(request.POST, request.FILES)

      if user_form.is_valid() and profile_form.is_valid():
         user = user_form.save(commit=False)
         user.is_owner = False
         user.save()
         user.customer_profile.company_name = profile_form.cleaned_data.get('company_name')
         user.customer_profile.website = profile_form.cleaned_data.get('website')
         user.customer_profile.image = profile_form.cleaned_data.get('images')
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

def show_profile(request):
   if request.user.is_authenticated:
      if request.user.is_owner:
         if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance = request.user)
            p_form =  OwnerUpdateForm(request.POST, request.FILES, instance = request.user.owner_profile)
            if u_form.is_valid() and p_form.is_valid():
               u_form.save()
               p_form.save()
               messages.success(request, f'Account has been update!')
               return redirect('launch:profile')
         else:
            u_form = UserUpdateForm(instance = request.user)
            p_form =  OwnerUpdateForm(instance = request.user.owner_profile)
         context = {
         'u_form': u_form,
         'p_form' : p_form
            }  
         return render(request, 'launch/profile.html',context)
 
      else:
         if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance = request.user)
            p_form =  CustomerUpdateForm(request.POST, request.FILES, instance = request.user.customer_profile)
            if u_form.is_valid() and p_form.is_valid():
               u_form.save()
               p_form.save()
               messages.success(request, f'Account has been update!')
               return redirect('launch:profile')
         else:
            u_form = UserUpdateForm(instance = request.user)
            p_form =  CustomerUpdateForm(instance = request.user.customer_profile)
         context = {
         'u_form': u_form,
         'p_form' : p_form
            }  
         return render(request, 'launch/profile.html',context)
   else:
      return redirect('launch:launch-home')




class RestaurantDetailView(DetailView):
   model = Restaurant

class RestaurantCreateView(LoginRequiredMixin,CreateView):
   login_url = '/login/'
   model = Restaurant
   fields = ['name', 'location', 'cuisine', 'image']

   def form_valid(self,form):
      form.instance.owner = self.request.user
      return super().form_valid(form)

class RestaurantUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
   login_url = '/login/'
   model = Restaurant
   fields = ['name', 'location', 'cuisine', 'image']

   def form_valid(self,form):
      form.instance.owner = self.request.user
      return super().form_valid(form)

   def test_func(self):
      restaurant = self.get_object()
      if self.request.user == restaurant.owner:
         return True
      else:
         return False

class RestaurantDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
   model = Restaurant
   success_url = '/'
   def test_func(self):
      restaurant = self.get_object()
      if self.request.user == restaurant.owner:
         return True
      else:
         return False



   