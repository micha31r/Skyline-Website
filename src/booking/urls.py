from django.urls import path
from . import views
from . import admin_views

app_name = "booking"

urlpatterns = [
    path('activities', views.activities_view, name="activities"),
    path('cart', views.cart_view, name="cart"),
    path('checkout/step1', views.checkout_step1_view, name="checkout-step1"),
    path('checkout/step2', views.checkout_step2_view, name="checkout-step2"),
    path('checkout/success', views.success_view, name="checkout-success"),
    path('checkout/success/<slug:success_id>', views.success_view, name="checkout-success"),
    
    # Admin section
    path('admin/all', admin_views.booking_list_view, name="admin-all"),
]