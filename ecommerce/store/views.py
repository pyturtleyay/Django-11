import stripe
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Product, Category
# from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import CartAddProductForm
from decimal import Decimal
from django.conf import settings
from store.models import Order
from django.shortcuts import render, redirect, reverse
from .models import OrderItem
from .forms import OrderCreateForm
from store.cart import Cart
from .tasks import order_created
from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from django.views.decorators.http import require_POST
from store.models import Product
from .forms import CartAddProductForm

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def store(request):
    return HttpResponse("Hello")


def user_login(request):

    # all_user = User.objects.all()
    # for user in all_user:
    #     print(user.username)

    if request.method == 'POST':
        userEmail = request.POST.get('userEmail')
        userPassword = request.POST.get('userPassword')
        print(userEmail, userPassword)
        user = authenticate(request, username=userEmail, password=userPassword)

        if user is not None:
            print("User available")
            if user.is_active:
                login(request, user)

                return redirect('/product_list')
            else:
                return HttpResponse('Disabled Account')
    return render(request, '/home/pyturtle_/Documents/ESHOPPING/ecommerce/store/templates/registration/login.html')


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


def profile(request):
    current_user = request.user
    return render(request, '/home/pyturtle_/Documents/ESHOPPING/ecommerce/store/templates/product/profile.html', {'user': current_user})


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

#PAYMENT
def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(
            reverse('payment:canceled'))
        # Stripe checkout session data
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        # add order items to the Stripe checkout session
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * Decimal('100')),
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
            })
        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        # redirect to Stripe payment form
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', locals())


def payment_completed(request):
 return render(request, 'payment/completed.html')


def payment_canceled(request):
 return render(request, 'payment/canceled.html')


#ORDER
def order_create(request):
	# get cart data 
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            print("Test")  
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            cart.clear()
            order_created.delay(order.id)
            request.session['order_id'] = order.id
            return redirect('')
    else:
        form = OrderCreateForm()
		# (by default) return render with template orders/order/created.html with cart data and form 
    return render(request, 'orders/create.html', {'cart':cart, 'form':form})
    # return render with template orders/order/create.html with order data 

#CART
@require_POST

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
        return redirect('cart:cart_detail')
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity' : item['quantity'],
            'override':True})
    return render(request, 'details.html', {'cart':cart})
