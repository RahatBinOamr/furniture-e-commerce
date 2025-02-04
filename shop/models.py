from autoslug import AutoSlugField
from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)

    def __str__(self):
        return self.name
class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='subcategories/', blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    session_key = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def total_price(self):
        return self.quantity * self.product.price
    
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)  
    session_key = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Customer"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    session_key = models.CharField(max_length=200, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"