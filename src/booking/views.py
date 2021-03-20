import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Activity
from .forms import UserInfoForm, PaymentForm

def activities_view(request):
	ctx = {}
	ctx["qs"] = Activity.objects.all().order_by("child_price")
	ctx["cart"] = cart = request.session.get("cart", [])
	if request.method == "POST":
		data = request.POST
		adult_count = data.get("adult_count", None)
		child_count = data.get("child_count", None)
		product_id = data.get("product_id", None)
		if adult_count and child_count and product_id:
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

def checkout_step1_view(request):
	ctx = {}
	ctx["cart"] = cart = request.session.get("cart", [])
	ctx["card_items_count"] = len(cart)
	ctx["total"] = 0
	for i in range(len(cart)):
		item = cart[i]
		cart[i]["total"] = total = item["adult_price"] * float(item["adult_count"]) + item["child_price"] * float(item["child_count"])
		ctx["total"] += total
	if request.method == "POST":
		form = UserInfoForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			info = {
				"first_name":data.get("first_name"),
				"last_name":data.get("last_name"),
				"email":data.get("email"),
				"phone":data.get("phone"),
				"date":data.get("date"),
				"date_repeat":data.get("date_repeat"),
			}
			request.session["user_info"] = json.dumps(info, default=str)
			return redirect("booking:checkout-step2")
	else:
		form = UserInfoForm()
	ctx["form"] = form
	template_file = "booking/checkout_step1.html"
	return render(request, template_file, ctx)

def checkout_step2_view(request):
	ctx = {}
	ctx["cart"] = cart = request.session.get("cart", [])
	ctx["card_items_count"] = len(cart)
	ctx["total"] = 0
	for i in range(len(cart)):
		item = cart[i]
		cart[i]["total"] = total = item["adult_price"] * float(item["adult_count"]) + item["child_price"] * float(item["child_count"])
		ctx["total"] += total
	if request.method == "POST":
		form = PaymentForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
	else:
		form = PaymentForm()
	ctx["form"] = form
	template_file = "booking/checkout_step2.html"
	return render(request, template_file, ctx)





