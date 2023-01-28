from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.store, name='store'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('cart/', views.cart, name='cart'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('product/', views.product, name='product'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.logout_view, name='logout'),
    path('product/<int:product_id>/', views.product_detail, name='product-detail'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('review/like/<int:review_id>', views.like_review, name='like_review'),


    #PAYPAL
    path('paypal/', include('paypal.standard.ipn.urls')),

    path('checkout_done/', views.checkout_done, name='checkout_done'),
    path('checkout/cancelled/', views.checkout_cancelled, name='checkout_cancelled'),


]+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)\
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
