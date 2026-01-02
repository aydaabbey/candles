from django.contrib import admin
from .models import Product, Order, OrderItem
from django.utils.timezone import now

# Display products within the order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Fields displayed in the main list
    list_display = [
        'id', 'first_name', 'phone', 'state', 
        'payment_method', 'paid', 'status', 'created'
    ]
    
    # Sidebar search filters
    list_filter = ['status', 'paid', 'payment_method', 'state', 'created']
    
    # Search fields
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'transaction_id']
    
    inlines = [OrderItemInline]
    
    # Add "Confirm Delivery" and "Mark as Paid" features for selected orders
    actions = ['mark_as_delivered', 'mark_as_paid']

    @admin.action(description='Confirm Delivery (Mark as Delivered)')
    def mark_as_delivered(self, request, queryset):
        # Upon delivery, update status and delivery date; if COD, mark as paid
        updated_count = queryset.update(
            status='delivered', 
            delivered_at=now(),
            paid=True # Automatically considered paid upon delivery (especially for COD)
        )
        self.message_user(request, f'Successfully marked {updated_count} orders as Delivered.')

    @admin.action(description='Mark as Paid')
    def mark_as_paid(self, request, queryset):
        updated_count = queryset.update(paid=True)
        self.message_user(request, f'{updated_count} orders were marked as paid.')

# Product registration
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name']