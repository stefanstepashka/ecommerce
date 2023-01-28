from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product, Review, Cart


class ProductTest(TestCase):
    def setUp(self):
        # Create 1000 test users
        for i in range(100000):
            User.objects.create(username='user{}'.format(i))

    def test_product_detail(self):
        # Retrieve a product
        product = Product.objects.first()

        # Retrieve reviews for the product
        reviews = Review.objects.filter(product=product)

        # Retrieve cart items for the product
        items = Cart.objects.filter(product=product)

        # Measure the performance of the queries
        # Use the timeit library to measure the time taken for the queries to execute
        import timeit
        review_query_time = timeit.timeit(lambda: reviews.all(), number=1000)
        item_query_time = timeit.timeit(lambda: items.all(), number=1000)

        # Print the query times
        print('Review query time:', review_query_time)
        print('Item query time:', item_query_time)