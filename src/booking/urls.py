from django.urls import path
from . import views

app_name = "booking"

urlpatterns = [
    path('activities', views.activities_view, name="activities"),
    path('cart', views.cart_view, name="cart"),
]