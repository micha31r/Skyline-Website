from django.conf import settings
from django.core.mail import send_mail
from background_task import background

@background(schedule=10)
def success_email(email, name, item_count, code, date):
    send_mail(
		f"Payment Success | Skyline NZ",
		f"👋 Thank you {name} for booking {item_count} activities at Skyline Rotorua. We are looking forward to seeing you on {date}. Here are your electronic tickets: \n http://localhost:8000/booking/checkout/success/{code}",
		settings.DEFAULT_FROM_EMAIL,
		[email],
		fail_silently=True,
	)