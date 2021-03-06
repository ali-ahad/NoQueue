from django.shortcuts import render, redirect,reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q
from django import forms
from .forms import UserForm, CustomerProfile
from .forms import CustomerProfileForm, OwnerProfileForm
from .forms import UserUpdateForm
from .forms import CustomerUpdateForm, PreForm
from .forms import OwnerUpdateForm
from .models import Restaurant, Item 
from .models import Order, OrderItem, Transaction, OwnerProfile
import random
import string
import datetime
from datetime import date



class RestaurantDetailView(DetailView):
   model = Restaurant

class RestaurantCreateView(CreateView):
   model = Restaurant
   fields = ['name', 'location', 'cuisine', 'description','image']

   def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(RestaurantCreateView, self).get_form(form_class)
        form.fields['name'].widget = forms.TextInput(attrs={'placeholder': 'Enter restaurant name'})
        form.fields['location'].widget = forms.TextInput(attrs={'placeholder': 'Enter location'})
        form.fields['cuisine'].widget = forms.TextInput(attrs={'placeholder': 'Enter cuisine type'})
        form.fields['description'].widget = forms.TextInput(attrs={'placeholder': 'Enter description'})
        return form

   def form_valid(self,form):
      user_profile = get_object_or_404(OwnerProfile, user=self.request.user)
      form.instance.owner = user_profile
      return super().form_valid(form)

class RestaurantUpdateView(UpdateView):
   login_url = '/login/'
   model = Restaurant
   fields = ['name', 'location', 'cuisine', 'description' ,'image']

   def get_form(self, form_class=None):
      if form_class is None:
            form_class = self.get_form_class()

      form = super(RestaurantUpdateView, self).get_form(form_class)
      form.fields['name'].widget = forms.TextInput(attrs={'placeholder': 'Enter restaurant name'})
      form.fields['location'].widget = forms.TextInput(attrs={'placeholder': 'Enter location'})
      form.fields['cuisine'].widget = forms.TextInput(attrs={'placeholder': 'Enter cuisine type'})
      form.fields['description'].widget = forms.TextInput(attrs={'placeholder': 'Enter description'})
      return form

   def form_valid(self,form):
      user_profile = get_object_or_404(OwnerProfile, user=self.request.user)
      form.instance.owner = user_profile
      return super().form_valid(form)

   def test_func(self):
      restaurant = self.get_object()
      if self.request.user == restaurant.owner:
         return True
      else:
         return False

class RestaurantDeleteView(DeleteView):
   model = Restaurant
   success_url = '/'
   def test_func(self):
      restaurant = self.get_object()
      if self.request.user == restaurant.owner:
         return True
      else:
         return False

# Function that works when launch page is accessed
class MenuDetailView(ListView):  
   def get_queryset(self):
      query = Item.objects.filter(restaurant = self.kwargs['pk'])
      if query:
         return query
      else:
         return Item.objects.none()


   
class ItemCreateView(CreateView):
   model = Item
   fields = ['name', 'price', 'description' ,'image']

   def get_form(self, form_class=None):
      if form_class is None:
         form_class = self.get_form_class()

      form = super(ItemCreateView, self).get_form(form_class)
      form.fields['name'].widget = forms.TextInput(attrs={'placeholder': 'Enter item name'})
      form.fields['price'].widget = forms.TextInput(attrs={'placeholder': 'Enter price'})
      form.fields['description'].widget = forms.TextInput(attrs={'placeholder': 'Enter description'})
      return form

   def form_valid(self,form):
      form.instance.restaurant = Restaurant.objects.get(pk = self.kwargs['pk'])
      return super().form_valid(form)


class ItemDetailView(DetailView):
   model = Item


class ItemUpdateView(UpdateView):
   login_url = '/login/'
   model = Item
   fields = ['name', 'price', 'description','image']

   def get_form(self, form_class=None):
      if form_class is None:
         form_class = self.get_form_class()

      form = super(ItemUpdateView, self).get_form(form_class)
      form.fields['name'].widget = forms.TextInput(attrs={'placeholder': 'Enter item name'})
      form.fields['price'].widget = forms.TextInput(attrs={'placeholder': 'Enter price'})
      form.fields['description'].widget = forms.TextInput(attrs={'placeholder': 'Enter description'})
      return form

   def form_valid(self,form):
      form.instance.restaurant = Restaurant.objects.get(pk = self.kwargs['rk'])
      return super().form_valid(form)

   def test_func(self):
      item = self.get_object()
      if self.request.user == item.restaurant.owner:
         return True
      else:
         return False
#LoginRequiredMixin,UserPassesTestMixin
class ItemDeleteView(DeleteView):
   model = Item
   success_url = '/'
   def test_func(self):
      item = self.get_object()
      if self.request.user == item.restaurant.owner:
         return True
      else:
         return False
         
def generate_order_id():
    date_str = date.today().strftime('%Y%m%d')[2:] + str(datetime.datetime.now().second)
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    return date_str + rand_str

@login_required()
def add_to_cart(request, **kwargs):
    # get the user profile
    user_profile = get_object_or_404(CustomerProfile, user=request.user)
    if user_profile:
      print('user retrieved!')
    # filter products by id
    item = Item.objects.filter(id=kwargs.get('pk')).first()
    if item in user_profile.cart.all():
      print('Already exists!')
      messages.info(request, 'You already own this ebook')
      return redirect(reverse('launch:item-detail', kwargs=kwargs)) 
    if item:
      print('Item retrived')
    # create orderItem of the selected product
    order_item, status = OrderItem.objects.get_or_create(item=item)
    if order_item:
      print('item handler!')
    if status:
      print('item handler status!')
   
    
    # create order associated with the user
    user_order = Order.objects.get_or_create(owner=user_profile, is_ordered=False)

    user_order.items.add(order_item)
   
    
    user_order.ref_code = generate_order_id()
    user_order.save()

 

    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect(reverse('launch:item-detail', kwargs=kwargs))

@login_required()
def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(CustomerProfile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0

@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('launch:order-summary'))

@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'launch/order_summary.html', context)


def update_transaction_records(request, token):
    # get the order being processed
    order_to_purchase = get_user_pending_order(request)

    # update the placed order
    order_to_purchase.is_ordered=True
    order_to_purchase.date_ordered=datetime.datetime.now()
    order_to_purchase.save()
    
    # get all items in the order - generates a queryset
    order_items = order_to_purchase.items.all()

    # update order items
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    # Add products to user profile
    user_profile = get_object_or_404(CustomerProfile, user=request.user)
    # get the products from the items
    order_products = [item.product for item in order_items]
    user_profile.ebooks.add(*order_products)
    user_profile.save()

    
    # create a transaction
    transaction = Transaction(profile=request.user.profile,
                            token=token,
                            order_id=order_to_purchase.id,
                            amount=order_to_purchase.get_cart_total(),
                            success=True)
    # save the transcation (otherwise doesn't exist)
    transaction.save()


    # send an email to the customer
    # look at tutorial on how to send emails with sendgrid
    messages.info(request, "Thank you! Your purchase was successful!")
    return redirect(reverse('launch:launch-home'))


def home(request):

   if request.user.is_authenticated:
      username = request.user.username

      if request.user.is_owner:
         user_profile = get_object_or_404(OwnerProfile, user=request.user)
         context = {
            'restaurants': Restaurant.objects.all(),
            'myrestaurants': Restaurant.objects.filter(owner = user_profile)
         }
         return render(request, 'launch/launch.html', context)

      else:
         context = {
            'restaurants': Restaurant.objects.all()   
         }
         return render(request, 'launch/launch.html',context)

   else:   
      return render(request, 'launch/launch.html')

# Navbar link functions
def about(request):
   return render(request, 'launch/about.html')

def contact(request):
   return render(request, 'launch/contact-us.html')

def blog_home(request):
   return render(request, 'launch/blog-home.html')

def blog_details(request):
   return render(request, 'launch/blog-details.html')

# Function for user registration
def register(request):
   return render(request, 'launch/register.html')

# Function that works when the chosen option is Restaurant owner
def register_owner(request):
   return render(request, 'launch/register-owner.html')

# Function that works when chosen option is customer owner
def register_customer(request):
   return render(request, 'launch/register-customer.html')

# Function that works then restuaurant owner registers
def owner_profile_view(request):
   if request.method == 'POST':
      user_form = UserForm(request.POST, prefix='UF')
      profile_form = OwnerProfileForm(request.POST, request.FILES, prefix='PF')

      if user_form.is_valid() and profile_form.is_valid():
         user = user_form.save(commit=False)
         user.save()
         username = user.username
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

  


# Function that works then customer registers
def customer_profile_view(request):
   if request.method == 'POST':
      user_form = UserForm(request.POST)
      profile_form = CustomerProfileForm(request.POST, request.FILES)

      if user_form.is_valid() and profile_form.is_valid():
         user = user_form.save(commit=False)
         user.is_owner = False
         user.save()
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

# Function that works when either the customer or restauarant owner's profile is shown
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

def show_cart(request):
   if request.user.is_authenticated:
      if not request.user.is_owner:
         customer = CustomerProfile.objects.filter(user = request.user)
         if customer:
            
            context = {
             'customer': customer
            }
            return render(request, 'launch/cart.html', context)

   else:
      return redirect('launch:launch-home')

def my_profile(request):
  my_user_profile = CustomerProfile.objects.filter(user=request.user).first()
  my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
  context = {
    'my_orders': my_orders
  }

  return render(request, "launch/profile.html", context)

def add_to_cart(request, **kwargs):
   # get the user profile
   user_profile = get_object_or_404(CustomerProfile, user=request.user)
   # filter products by id
   product = Item.objects.filter(id=kwargs['pk']).first()
   print('Product is!')
   print(product.name)
   # create orderItem of the selected product
   order_item, status = OrderItem.objects.get_or_create(product=product, is_ordered= False)
   print('Item is!')
   print(order_item)
   if status:
      print('First status!')

   # create order associated with the user

   user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
   
   # check if the user already owns this product
   if order_item in user_order.items.all():
      order_item.quantity = order_item.quantity + 1
      order_item.save()
      print('alreayd own!')
      print(user_order.items.get(pk=order_item.pk).quantity)
      messages.info(request, 'You already own this ebook')
      return redirect(reverse('launch:restaurant-menu', kwargs = {'pk': product.restaurant.pk }))

   user_order.items.add(order_item)
   #user_order.items=order_item
   if status:
      # generate a reference code
      user_order.ref_code = 1
      user_order.save()

   print("-----------ORDER CHECK-----------")
   print("USER ORDER ITEMS: " + str(user_order.items.all()))
   print("-----------ORDER CHECK END-----------")

   # show confirmation message and redirect back to the same page
   messages.info(request, "item added to cart")
   return redirect(reverse('launch:restaurant-menu', kwargs={'pk':product.restaurant.pk})) 


def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(CustomerProfile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0



def order_details(request, **kwargs):
  if request.user.is_authenticated and not request.user.is_owner:
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'launch/order_summary.html', context)
  else:
    return render(request, 'launch:order-summary')


def delete_from_cart(request, **kwargs):
    item_to_delete = OrderItem.objects.get(pk=kwargs['pk'])
    if item_to_delete:
        if item_to_delete.quantity > 1:
          item_to_delete.quantity = item_to_delete.quantity - 1
          item_to_delete.save()
        else:
          item_to_delete.delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('launch:order-summary'))

def search(request):
   template = 'launch/launch.html'
   query = request.GET.get('q')

   if query:
      results = Restaurant.objects.filter(name__icontains=query)
      print(results)
   else:
      results = Restaurant.objects.all()

   context = {
      'restaurants': results
   }


   return render(request, template,context)

def insertTransaction(request, **kwargs):
   user_profile = get_object_or_404(CustomerProfile, user=request.user)
   orders = Order.objects.filter(owner=user_profile, is_ordered=False)
   result = orders.all()
   token = "1234"
   new_ref = 0

   print("LOLz")

   for i, order in enumerate(result):
      print(i)
      order.is_ordered=True
      OrderItems = order.items.all()
      for item in OrderItems:
         print("ORDER QUANTITY: "+str(item.quantity))
         item.is_ordered = True
         item.save()
      new_ref = int(order.ref_code)
      order.save()
      
      restaurant = order.items.first().product.restaurant
      owner = restaurant.owner
      print("Restaurant pk: "+str(restaurant.pk))
      print("Restaurant name: "+str(restaurant.name))
      timestamp = datetime.datetime.now()
      print("Timestamp: " + str(timestamp))
      print("Owner: " + str(owner.user.username))
      price = order.get_cart_total()
      trans = Transaction(profile = user_profile, order = order, restaurant = restaurant, timestamp = timestamp, owner =owner, price = price)
      trans.save()
      new_ref+=1
      new_ref=str(new_ref)
      order= Order(owner=user_profile, is_ordered=False, ref_code = new_ref)
      order.save()

      print("-----------------CHECK--------------------")
      print("Restaurant name: "+str(trans.restaurant.name))
      print("Order: "+str(trans.order.items))
      print("-----------------CHECK END--------------------")


      return redirect('launch:dateForm')


def displayOrderHistoryCustomer(request, **kwargs):
   user_profile = get_object_or_404(CustomerProfile, user=request.user)
   transactions = Transaction.objects.filter(profile = user_profile).all()
   orders = list()


   for transaction in transactions:
      orders.append(transaction.order.items)

   for order in orders:
      print(order)



   if request.user.is_authenticated:
      context ={
         'Transactions': transactions
      }

   return render(request, 'launch/orders.html', context)


def displayReceivedOrders(request, **kwargs):
   owner_profile = get_object_or_404(OwnerProfile, user=request.user)

   transactions = Transaction.objects.filter(owner = owner_profile).all()
   if request.user.is_authenticated:
      context = {
         'Transactions' : transactions
      }

      print("------------REACHED------------")

   return render(request, 'launch/orders.html', context)

def recommendation(request, **kwargs):

   user_profile = get_object_or_404(CustomerProfile, user=request.user)
   Owner_list = OwnerProfile.objects.all()
   recommendations = []
   owner_range = len(Owner_list)
   rec_count =0
   print("Owner count: "+ str(len(Owner_list)))



   for owners1 in Owner_list:
      RestaurantList = Restaurant.objects.filter(owner = owners1).all()
      owner_rest_range = len(RestaurantList)
      i = 0
      if(owner_rest_range > 0 and rec_count<=3):
         rec_count+=1
         random_list = random.randint(0, owner_rest_range-1)
         recommendations.append(RestaurantList[random_list])
      else:
         continue
   
   if(rec_count==0):
      print("No restaurants available")
   else:
      for restaurant in recommendations:
         print("Restaurant name: " + str(restaurant.name) )
         print("Restaurant owner: " + str(restaurant.owner))
   if request.user.is_authenticated:
      context ={
      'recommendation': recommendations
      }
      
      print("Context: ", context )

   return render(request, 'launch/recommendationPage.html', context)


def dateForm(request):
   date_forms = PreForm(request.POST)
   if date_forms.is_valid():
      Date = str(date_forms['year'].value())+"-"+str(date_forms['month'].value())+"-"+str(date_forms['day'].value())+" "+str(date_forms['hour'].value())+":"+str(date_forms['min'].value())+":"+"00"
      print(Date)
      Date = datetime.datetime.strptime(Date, '%Y-%m-%d %H:%M:%S')
      print("Date time: ", Date)

      user_profile = get_object_or_404(CustomerProfile, user=request.user)
      transactions = Transaction.objects.filter(profile = user_profile, isTransacted=False).first()
      transactions.collect_timestamp=Date
      transactions.isTransacted =True
      transactions.save()


      return render( request,'launch/purchase_success.html')
        
   else:
      user_form = UserForm(prefix='UF')
      profile_form = OwnerProfileForm(prefix='PF')

      return render(request, 'launch/dateform.html',{
      'date_form': date_forms,})
   
def updateStatusAccept(request, **kwargs):
   transactions = Transaction.objects.get(pk=kwargs['pk'])

   print("Transaction: ", transactions)
   transactions.orderStatus = 'Accepted'
   transactions.save()

   return redirect("launch:owner-order")

def updateStatusReject(request, **kwargs):
   transactions = Transaction.objects.get(pk=kwargs['pk'])

   print("Transaction: rejection", transactions)
   transactions.orderStatus = 'Rejected'
   transactions.save()

   return redirect("launch:owner-order")
