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
			obj = Activity.objects.get(product_id=product_id)
			cart.append({
				"name":obj.name,
				"description":obj.description,
				"adult_price":obj.adult_price,
				"child_price":obj.child_price,
				"product_id":product_id,
				"adult_count":adult_count,
				"child_count":child_count,
			})
			request.session["cart"] = cart
	template_file = "booking/activities.html"
	return render(request, template_file, ctx)

def cart_view(request):
	ctx = {}
	ctx["cart"] = cart = request.session.get("cart", [])
	ctx["card_items_count"] = len(cart)
	ctx["total"] = 0
	for i in range(len(cart)):
		item = cart[i]
		cart[i]["total"] = total = item["adult_price"] * float(item["adult_count"]) + item["child_price"] * float(item["child_count"])
		ctx["total"] += total
	if request.method == "POST":
		data = request.POST
		adult_count = data.get("adult_count", None)
		child_count = data.get("child_count", None)
		product_id = data.get("product_id", None)
		if adult_count and child_count and product_id:
			cart = request.session.get("cart", [])
			for i in range(len(cart)):
				v = cart[i]
				if v["adult_count"] == adult_count and v["child_count"] == child_count and v["product_id"] == product_id:
					del cart[i]
					break
			request.session["cart"] = cart
	template_file = "booking/cart.html"
	return render(request, template_file, ctx)