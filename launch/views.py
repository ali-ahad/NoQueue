from django.shortcuts import render, redirect,reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.conf import settings
from .forms import UserForm, CustomerProfile
from .forms import OwnerProfileForm
from .forms import CustomerProfileForm
from .forms import UserUpdateForm
from .forms import CustomerUpdateForm
from .forms import OwnerUpdateForm
from .models import Restaurant, Item 
from .models import Order, OrderItem, Transaction
import random
import string
import datetime
import braintree
import stripe
from datetime import date

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=settings.BT_ENVIRONMENT,
        merchant_id=settings.BT_MERCHANT_ID,
        public_key=settings.BT_PUBLIC_KEY,
        private_key=settings.BT_PRIVATE_KEY
    )
)

stripe.api_key = settings.STRIPE_SECRET_KEY

class RestaurantDetailView(DetailView):
   model = Restaurant

class RestaurantCreateView(CreateView):
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
   fields = ['name', 'price', 'cuisine', 'image']

   def form_valid(self,form):

      form.instance.restaurant = Restaurant.objects.get(pk = self.kwargs['pk'])
      return super().form_valid(form)


class ItemDetailView(DetailView):
   model = Item


class ItemUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
   login_url = '/login/'
   model = Item
   fields = ['name', 'price', 'cuisine', 'image']

   def form_valid(self,form):
      form.instance.restaurant = Restaurant.objects.get(pk = self.kwargs['rk'])
      return super().form_valid(form)

   def test_func(self):
      item = self.get_object()
      if self.request.user == item.restaurant.owner:
         return True
      else:
         return False

class ItemDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
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

def generate_client_token():
    return gateway.client_token.generate()

def transact(options):
    return gateway.transaction.sale(options)

def find_transaction(id):
    return gateway.transaction.find(id)


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
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)

    user_order.items.add(order_item)
    
    if status:
        # generate a reference code
      print('status retrived!')
    user_order.ref_code = generate_order_id()
    user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect(reverse('launch:item-detail', kwargs=kwargs))

def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(CustomerProfile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0

def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('launch:order_summary'))

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
    return redirect(reverse('accounts:my_profile'))

def checkout(request, **kwargs):
   client_token = generate_client_token()
   existing_order = get_user_pending_order(request)
   publishKey = settings.STRIPE_PUBLISHABLE_KEY
   if request.method == 'POST':
      token = request.POST.get('stripeToken', False)
      if token:
         try:
            charge = stripe.Charge.create(
               amount=100*existing_order.get_cart_total(),
               currency='usd',
               description='Example charge',
               source=token,
            )

            return redirect(reverse('launch:item-update', 
                     kwargs={
                        'token': token
                     }))
         except stripe.error.CardError as e:
            messages.info(request, e)

      else:
         result = transact({
            'amount': existing_order.get_cart_total(),
            'payment_method_nonce': request.POST['payment_method_nonce'],
            'options': {
               "submit_for_settlement": True
            }
         })

         if result.is_success or result.transaction:
            return redirect(reverse('launch:item-update', 
                     kwargs={
                        'token': result.transaction.id
                     }))

         else: 
            for x in result.errors.deep_errors:
               messages.info(request, x)
            return redirect(reverse('launch:item-update'))

   context = {
      'order': existing_order,
      'client_token': client_token,
      'STRIPE_PUBLISHABLE_KEY': publishKey
   }

   return render(request, 'launch/checkout.html', context)


def success(request, **kwargs):
    # a view signifying the transcation was successful
    return render(request, 'shopping_cart/purchase_success.html', {})






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
    order_item, status = OrderItem.objects.get_or_create(product=product)
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
    if status:
        # generate a reference code
        user_order.ref_code = 1
        user_order.save()

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
    return render(request, 'launch:launch-home')


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



   