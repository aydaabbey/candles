from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # 1. Shop and product display
    path('', views.product_list, name='product_list'),
    
    # 2. Shopping cart management
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    
    # 3. Checkout process
    path('order/create/', views.order_create, name='order_create'),
    
    # 4. Customer account and order history
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
]