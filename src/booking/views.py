from django.shortcuts import render
from .models import Activity

def activities_view(request):
	ctx = {}
	ctx["qs"] = Activity.objects.all().order_by("child_price")
	if request.method == "POST":
		data = request.POST
		adult_count = data.get("adult_count", None)
		child_count = data.get("child_count", None)
		product_id = data.get("product_id", None)
		if adult_count and child_count and product_id:
			cart = request.session.get("cart", [])
			cart.append({
				"id":product_id,
				"adult_count":adult_count,
				"child_count":child_count,
			})
			request.session["cart"] = cart
			print(cart)
	template_file = "booking/activities.html"
	return render(request, template_file, ctx)