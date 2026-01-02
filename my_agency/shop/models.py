from django.db import models
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price in Malaysian Ringgit (RM)
    image = models.ImageField(upload_to='products/')
    
    def __str__(self):
        return self.name

class Order(models.Model):
    # Official list of Malaysian States
    MALAYSIA_STATES = (
        ('Johor', 'Johor'),
        ('Kedah', 'Kedah'),
        ('Kelantan', 'Kelantan'),
        ('Melaka', 'Melaka'),
        ('Negeri Sembilan', 'Negeri Sembilan'),
        ('Pahang', 'Pahang'),
        ('Perak', 'Perak'),
        ('Perlis', 'Perlis'),
        ('Pulau Pinang', 'Pulau Pinang'),
        ('Sabah', 'Sabah'),
        ('Sarawak', 'Sarawak'),
        ('Selangor', 'Selangor'),
        ('Terengganu', 'Terengganu'),
        ('Kuala Lumpur', 'W.P. Kuala Lumpur'),
        ('Labuan', 'W.P. Labuan'),
        ('Putrajaya', 'W.P. Putrajaya'),
    )

    # Updated payment options (COD added)
    PAYMENT_METHODS = (
        ('card', 'Credit / Debit Card'),
        ('fpx', 'Online Banking (FPX)'),
        ('ewallet', 'E-Wallet (TNG, GrabPay, Boost)'),
        ('cod', 'Cash on Delivery (COD)'), # Pay on receipt
    )

    # Order and Delivery statuses
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'), # Successfully received
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='orders', null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Malaysian address details
    address = models.CharField(max_length=250)
    postcode = models.CharField(max_length=10) # Postcode
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50, choices=MALAYSIA_STATES, default='Selangor')
    
    # Timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    delivered_at = models.DateTimeField(null=True, blank=True) # Actual delivery date
    
    # Payment and delivery status
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='fpx')
    transaction_id = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Item {self.id} for Order {self.order.id}'

    def get_cost(self):
        return self.price * self.quantity