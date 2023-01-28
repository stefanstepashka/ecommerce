from django.core.paginator import Paginator
from .forms import ProductFiltersform, RegistrationForm, AuthenticationForm, AddToCartForm, ContactForm, ReviewForm, ReplyForm
from .models import Product, Cart, Order, Contact, Review
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.core.mail import send_mail
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
import uuid
from django.conf import settings
from django.db.models import Avg

PAYPAL_CLIENT_ID = settings.PAYPAL_CLIENT_ID
PAYPAL_CLIENT_SECRET = settings.PAYPAL_CLIENT_SECRET





def store(request):
    product = Product.objects.all()
    items = []
    if request.user.is_authenticated:
        items = Cart.objects.filter(user=request.user)

    context = {
        'products': product,
        'items': items
    }
    return render(request, 'store/index.html', context)


def checkout(request):
    items = []
    if request.user.is_authenticated:
        # Get all the items in the user's cart
        items = Cart.objects.filter(user=request.user)

        total = 0
        for item in items:
            total += item.product.price * item.quantity

        ftotal = round(total, 2)

        # Total amount of items
        total_amount = sum([item.total_price() for item in items])

        # Get the names of the items
        item_names = ', '.join([item.product.name for item in items])
        paymentId = uuid.uuid4()
        # Create the PayPal payment form
        form = PayPalPaymentsForm(initial={
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": total_amount,
            "currency_code": "USD",
            "item_name": item_names,
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return_url": request.build_absolute_uri(reverse('checkout_done')),
            "cancel_return": request.build_absolute_uri(reverse('checkout_cancelled')),
            "form_action": "https://www.paypal.com/cgi-bin/webscr",  # Use this for live transactions
            "form_target": "_blank",
        })

        # Render the template and pass the items and form as context
        return render(request, 'store/checkout.html',
                      {'form': form, 'items': items, 'total': ftotal, 'total_amount': total_amount})
    else:
        # Redirect the user to the login page if they are not authenticated
        return redirect('login')


def checkout_done(request):
    items = []
    items = Cart.objects.filter(user=request.user)
    total_amount = sum([item.total_price() for item in items])
    payment_id = request.GET.get('paymentId')

    order = Order.objects.create(
        customer=request.user,
        total_price=total_amount,
        status='PAID',
        payment_id=payment_id,
    )
    # Add the products to the order
    products = [item.product for item in Cart.objects.filter(user=request.user)]
    order.products.set(products)
    order.save()

    if order.total_price == 0:
        order.delete()
        return redirect('store')

    # Clear the cart and redirect to the order confirmation page
    Cart.objects.filter(user=request.user).delete()
    # Clear the cart and redirect to the order con
    return render(request, 'store/order_confirmation.html')


def checkout_cancelled(request):

    return redirect('checkout')


def product(request):
    items = []
    products = Product.objects.all()
    search_query = request.GET.get('q')
    form1 = ProductFiltersform()
    form = AddToCartForm()
    category = request.GET.get('category')
    if search_query:
        products = Product.objects.filter(name__icontains=search_query)
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():

            quantity = form.cleaned_data.get('quantity')
            cart = Cart(user=request.user, product=product, quantity=quantity)
            cart.save()
            return redirect('cart')
    else:
        # Process the form when the request method is GET
        form1 = ProductFiltersform(request.GET)
        if form1.is_valid():
            category = form1.cleaned_data.get('category')
            if category and category != 'all':
                products = products.filter(category=category)

    per_page = 3
    if request.user.is_authenticated:
        items = Cart.objects.filter(user=request.user).prefetch_related('product')
        user_id = request.user.pk

    else:
        user_id = None
    # Create a paginator object for the products
    paginator = Paginator(products, per_page)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    context = {
        'products': products_page,
        'form1': form1,
        'form': form,
        'paginator': paginator,
        'page_number': page_number,
        'products_page': products_page,
        'items': items,


    }
    return render(request, 'store/product.html', context)



def product_detail_page(request):
    context = {}
    return render(request, 'store/product-detail.html', context)


def logout_view(request):
    logout(request)
    return redirect('store')


def product_detail(request, product_id):
    items = []
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(user=request.user.pk, product=product).select_related()
    items = Cart.objects.filter(user=request.user.pk)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    if request.user.is_authenticated:
        if request.method == 'POST':
            # Bind the form to the POST data
            form = AddToCartForm(request.POST)
            reviewform = ReviewForm(request.POST)
            repform = ReplyForm(request.POST)

            if form.is_valid():
                # Get the quantity from the form
                quantity = form.cleaned_data['quantity']
                # Create a new Cart object and save it to the database
                cart = Cart(user=request.user, product=product, quantity=quantity)
                cart.save()

                # Redirect the user to the cart page
                return redirect('cart')
            elif reviewform.is_valid():
                existing_review = Review.objects.filter(product=product, user=request.user).first()
                if existing_review:
                    # Return an error message if the user has already reviewed this product
                    return render(request,
                                  'store/product-detail.html',
                                  {'product': product, 'items': items, 'form': form,
                                   'reviewform': reviewform, 'reviews': reviews,
                                   'avg_rating': avg_rating,
                                   'error': 'You have already reviewed this product'})

                    # Save the review if the user has not reviewed this product yet
                review_text = reviewform.cleaned_data['review_text']
                review_rating = reviewform.cleaned_data['rating']
                review = Review(user=request.user,
                                product=product,
                                rating=review_rating,
                                review_text=review_text)
                review.save()
                return redirect('product-detail', product_id=product.id)
            elif repform.is_valid():
                review_id = request.POST.get('review_id', None)
                if review_id is not None:
                    review = get_object_or_404(Review, pk=review_id)
                    reply = repform.save(commit=False)
                    reply.review = review
                    reply.user = request.user
                    reply.save()
                    return redirect('product-detail', product_id=review.product.id)
                else:
                    # Handle the case where review_id is not present in the POST request
                    pass
            else:
                form = AddToCartForm()
                reviewform = ReviewForm()
                repform = ReplyForm()
        else:
            form = AddToCartForm()
            reviewform = ReviewForm()
            repform = ReplyForm()
    else:
        return redirect('login')

    # Render the product_detail template and pass the product object to the template
    return render(request, 'store/product-detail.html', {'product': product, 'items': items, 'form': form,
                                                         'reviewform': reviewform, 'reviews': reviews,
                          'avg_rating': avg_rating, 'repform': repform,})


from django.http import JsonResponse


def like_review(request, review_id):
    if request.method == 'POST':
        # Only allow authenticated users to like a review
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'You must be logged in to like a review.'})

        # Get the review object
        review = get_object_or_404(Review, pk=review_id)
        user = request.user

        # Check if the user has already liked the review
        if user in review.likes.all():
            review.likes.remove(user)
            review.save()
            is_liked = False
        else:
            review.likes.add(user)
            review.save()
            is_liked = True

        # Return a JSON response indicating whether the like was added successfully
        return JsonResponse({'status': 'success', 'is_liked': is_liked})



def remove_from_cart(request, product_id):
    # Get the product object

    product = get_object_or_404(Product, pk=product_id)

    # Get the cart object for the current user and the product
    cart = Cart.objects.filter(user=request.user, product=product).first()

    # Delete the cart object from the database
    cart.delete()

    # Redirect the user back to the cart page
    return redirect('cart')


def cart(request):
    items = []
    if request.user.is_authenticated:

        # Get all the items in the user's cart
        items = Cart.objects.filter(user=request.user)

        total = 0
        for item in items:
            total += item.product.price * item.quantity

        ftotal = round(total, 2)
        # Render the template and pass the items as context
        return render(request, 'store/cart.html', {'items': items, 'total': ftotal})
    else:
        # Redirect the user to the login page if they are not authenticated
        return redirect('login')



def about(request):
    items = []
    if request.user.is_authenticated:

        # Get all the items in the user's cart
        items = Cart.objects.filter(user=request.user)
    context = {'items': items}
    return render(request, 'store/about.html', context)


def contact(request):
    if request.user.is_authenticated:

        # Get all the items in the user's cart
        items = Cart.objects.filter(user=request.user)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            contact = Contact(full_name=full_name, subject=subject, email=email, message=message)
            contact.save()

            send_mail(
                subject,  # Subject
                message,  # Message
                'bidzhamov.stevens@mail.ru',  # From email
                ['bidzhamov.stevens@mail.ru'],  # List of recipient emails
            )

            # Send email
            messages.add_message(request, messages.SUCCESS, 'Your message was sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'store/contact.html', {'form': form, 'items': items})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():

            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'store/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('store')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

