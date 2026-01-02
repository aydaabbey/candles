from django.db import models
# Import the Product model from the shop app
from shop.models import Product 

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='portfolio/images/')
    url = models.URLField(blank=True)
    # Link the project to a specific product (optional)
    related_product = models.ForeignKey(
        Product, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Related Product"
    )

    def __str__(self):
        return self.title