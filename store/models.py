from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.contrib.auth import get_user_model


class Product(models.Model):

    CATEGORY = (
        ('vodka', 'Vodka'),
        ('whiskey', 'Whiskey'),
        ('rum', 'Rum'),
        ('gin', 'Gin'),
        ('wine', 'Wine')

    )
    name = models.CharField(max_length=40)
    price = models.FloatField()
    image = models.ImageField(default=False)
    digital = models.BooleanField(default=False, blank=True, null=True)
    category = models.CharField(
        max_length=40,
        choices=CATEGORY,
    )

    def __str__(self):
        return self.name


    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return self.product.name


class Order(models.Model):
    carts = models.ManyToManyField(Cart)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=9, decimal_places=2)
    date_placed = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255)
    payment_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.status


class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    review_text = models.TextField(max_length=185)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='review_likes', blank=True)

    def total_likes(self):
        return self.likes.count()


class Reply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_text = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.reply_text

