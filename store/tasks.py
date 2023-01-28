
import celery
from .models import Product
from .views import *
from celery import shared_task





@shared_task(time_limit=10)
def search_task(query, category):
    # Perform the search here
    products = Product.objects.all()
    if category and category != 'all':
        products = products.filter(category=category)
    if query:
        products = products.filter(name__icontains=query)

    # Return the search results
    return products
