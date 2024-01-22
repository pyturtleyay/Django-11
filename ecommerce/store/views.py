from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Product, Category
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from cart.forms import CartAddProductForm

def store(request):
    return HttpResponse("Hello")

def user_login(request):

    # all_user = User.objects.all()
    # for user in all_user:
    #     print(user.username)

    if request.method=='POST':
        userEmail = request.POST.get('userEmail')
        userPassword = request.POST.get('userPassword')
        print(userEmail, userPassword)
        user = authenticate(request, username = userEmail, password = userPassword)

        if user is not None:
            print("User available")
            if user.is_active:
                login(request, user)

                return redirect('/product_list')
            else:
                return HttpResponse('Disabled Account')    
    return render(request, '/home/pyturtle_/Documents/ESHOPPING/ecommerce/store/templates/registration/login.html')



def product_detail(request, id ,slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'product/detail.html', 
                            {'product':product,
                            'cart_product_form':cart_product_form})
def profile(request):
    current_user = request.user
    return render(request, '/home/pyturtle_/Documents/ESHOPPING/ecommerce/store/templates/product/profile.html', {'user':current_user})

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