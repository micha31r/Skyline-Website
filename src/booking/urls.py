from django.urls import path
from . import views
from . import activity_views
from . import admin_views

app_name = "booking"

urlpatterns = [
    # Booking pages
    path('activities', views.activities_view, name="activities"),
    path('cart', views.cart_view, name="cart"),
    path('checkout/step1', views.checkout_step1_view, name="checkout-step1"),
    path('checkout/step2', views.checkout_step2_view, name="checkout-step2"),
    path('checkout/success', views.success_view, name="checkout-success"),
    path('checkout/success/<slug:success_id>', views.success_view, name="checkout-success"),
    
    # Activity details pages
    path('luge', activity_views.LugeView.as_view(), name="luge"),

    # Admin pages
    path('admin/all', admin_views.booking_list_view, name="admin-all"),
    path('admin/edit/<slug:user_slug>/<int:ticket_id>', admin_views.booking_edit_view, name="admin-edit"),
    path('admin/edit/<slug:user_slug>/<int:ticket_id>/activate', admin_views.booking_activate_view, name="admin-edit-activate"),
    path('admin/edit/<slug:user_slug>/<int:ticket_id>/void', admin_views.booking_void_view, name="admin-edit-void"),
]