from django.contrib import admin
from .models import Product, Cart, Review, Order

admin.site.register(Product)

admin.site.register(Cart)
admin.site.register(Review)
admin.site.register(Order)