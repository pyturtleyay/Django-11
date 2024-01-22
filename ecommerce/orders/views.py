
from django.shortcuts import render, redirect, reverse
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
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

#...


