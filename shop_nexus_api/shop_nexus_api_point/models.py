from django.db import models
from django.contrib.auth.models import User, auth
import uuid

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    bio = models.CharField(max_length=255)
    about = models.TextField(max_length=255)
    rating = models.IntegerField()
    business_name = models.CharField(max_length=255)
    business_category = models.CharField(max_length=255)
    business_reg_no = models.CharField(max_length=255)
    business_logo = models.ImageField(upload_to='logo_images/')

    def __str__(self):
        return self.business_name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.user.username


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', default='no-product-img.png')
    img_1 = models.ImageField(upload_to='product_images/', default='no-product-img.png')
    img_2 = models.ImageField(upload_to='product_images/', default='no-product-img.png')
    img_3 = models.ImageField(upload_to='product_images/', default='no-product-img.png')
    img_4 = models.ImageField(upload_to='product_images/', default='no-product-img.png')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    count = models.IntegerField(default=0)
    rating = models.IntegerField()
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity}"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    orderitem_list = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id}"

class Jwt(models.Model):
    user = models.OneToOneField(
        User, related_name="login_user", on_delete=models.CASCADE)
    access = models.TextField()
    refresh = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{User.objects.get(id=self.user.id)}"

class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=100)
    # Add other fields as needed

    def __str__(self):
        return f"Payment ID: {self.id}, User: {self.customer.name}, Amount: {self.amount}, Status: {self.status}"


