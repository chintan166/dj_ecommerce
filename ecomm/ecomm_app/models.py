from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200,null=True)
    contact = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)  # Unique name for each category
    description = models.TextField(null=True, blank=True)  # Optional description field
    slug = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name  # Display the category name in the admin


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)  # Field to store the available quantity in stock.
    colors = models.ManyToManyField('Color',blank=True, related_name='products')  # Many-to-many relationship with Color


    def __str__(self):
        return self.name
    
    def check_availability(self, qty):
        """Check if the requested quantity is available in stock."""
        if qty <= self.stock:
            return True  # The requested quantity is available
        else:
            return False  # Insufficient stock
        
    def update_stock(self, qty):
        """Update the stock after a purchase."""
        if qty <= self.stock:
            self.stock -= qty
            self.save()
            return True  # Stock updated successfully
        else:
            return False  # Not enough stock to update
        
class Color(models.Model):
    name = models.CharField(max_length=100,blank=True)
    hex_code = models.CharField(max_length=7,blank=True)  # e.g. #FF5733 for color

        # Many-to-many relationship with color options
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/gallery/', null=True, blank=True)
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - Image {self.id}"
    
class ShippingMethod(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - ${self.price}"
    
class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')
    
    # Addresses
    billing_address = models.CharField(max_length=255)
    shipping_address = models.CharField(max_length=255)
    
    # Shipping method
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True)
    
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="orderitems", on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='orderitems', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)  # Add color field

    
    def total_price(self):
        return self.quantity * self.price



class Cart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Use get_user_model() here
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    @property
    def total_price(self):
        return self.product.price * self.quantity

class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


