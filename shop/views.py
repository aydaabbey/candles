from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem
from .forms import OrderCreateForm
from .cart import Cart
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# 1. Display product list
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

# 2. Add product to cart
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('shop:cart_detail')

# 3. Remove product from cart
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')

# 4. Display cart details (This is the function that was missing and caused the error)
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart_detail.html', {'cart': cart})

# 5. Create Order (Checkout)
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return render(request, 'shop/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'shop/order_create.html', {'cart': cart, 'form': form})

# 6. Customer Dashboard
@login_required
def customer_dashboard(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/dashboard.html', {'orders': orders})