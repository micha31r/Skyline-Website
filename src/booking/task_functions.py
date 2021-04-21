from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from background_task import background
from django.db.models import Q
from .models import Ticket

@background(schedule=10)
def success_email(email, name, item_count, code, date):
    send_mail(
		f"Payment Success | Skyline NZ",
		f"👋 Thank you {name} for booking {item_count} activities at Skyline Rotorua. We are looking forward to seeing you on {date}. Here are your electronic tickets: \n http://localhost:8000/booking/checkout/success/{code}",
		settings.DEFAULT_FROM_EMAIL,
		[email],
		fail_silently=True,
	)

@background(schedule=0)
def remove_expired_tickets():
	# Delete expired, voided, or activated tickets after 90 days
	limit = (timezone.now() - timedelta(days=90)).date()
	lookups = Q(activation_date__lt=limit) | \
		Q(expected_activation_date__lt=limit) | \
		Q(void_date__lt=limit)
	qs = Ticket.objects.filter(lookups).delete()