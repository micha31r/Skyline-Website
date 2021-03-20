from django.urls import path
from . import views

app_name = "booking"

urlpatterns = [
    path('activities', views.activities_view, name="activities"),
    path('cart', views.cart_view, name="cart"),
    path('checkout/step1', views.checkout_step1_view, name="checkout-step1"),
    path('checkout/step2', views.checkout_step2_view, name="checkout-step2"),
]