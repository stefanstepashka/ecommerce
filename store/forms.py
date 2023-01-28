from django import forms
from .models import Product
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Cart, Contact, Review, Reply
from paypal.standard.forms import PayPalPaymentsForm
#To filter categories

class ProductFiltersform(forms.Form):
    CATEGORY_CHOICES = (
        ('all', 'All'),
        ('vodka', 'Vodka'),
        ('whiskey', 'Whiskey'),
        ('rum', 'Rum'),
        ('gin', 'Gin'),
        ('wine', 'Wine')
    )
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False)


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']


class CartUpdateForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']

#...........REGISTRATION...........



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    address = forms.CharField(max_length=200)
    postal_code = forms.CharField(max_length=20)


class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)


class ReviewForm(forms.Form):
    review_text = forms.CharField(widget=forms.Textarea)
    rating = forms.IntegerField(min_value=1, max_value=5)

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply_text']