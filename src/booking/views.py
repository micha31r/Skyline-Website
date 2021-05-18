import datetime
from datetime import timedelta
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from usermgmt.models import Profile
from .models import Activity, Ticket
from .forms import UserInfoForm, PaymentForm, UserIdentifyForm
from .task_functions import success_email

def activities_view(request):
	ctx = {}
	ctx["qs"] = Activity.objects.all().order_by("child_price")
	ctx["cart"] = cart = request.session.get("cart", [])
	if request.method == "POST":
		# Get form data
		data = request.POST
		adult_count = data.get("adult_count", None)
		child_count = data.get("child_count", None)
		product_id = data.get("product_id", None)
		if adult_count and child_count and product_id:
			if adult_count.isdigit() and child_count.isdigit() and (int(adult_count) > 0 or int(child_count) > 0):
				# Save item to cart
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
				abs_link = reverse('booking:cart')
				messages.info(request, f"Successfully added '{obj.name}' to cart. <a href='{abs_link}'>Continue to checkout?</a>")
			else:
				messages.error(request, f"Number of children / adults must be greater than zero")
	template_file = "booking/activities.html"
	return render(request, template_file, ctx)

def cart_view(request):
	ctx = {}
	# Get card data from session
	ctx["cart"] = cart = request.session.get("cart", [])
	ctx["card_items_count"] = len(cart)
	ctx["total"] = 0
	# Calculate the total cost of all cart items
	for i in range(len(cart)):
		item = cart[i]
		cart[i]["total"] = total = item["adult_price"] * float(item["adult_count"]) + item["child_price"] * float(item["child_count"])
		ctx["total"] += total
	if request.method == "POST":
		# Get form data
		data = request.POST
		adult_count = data.get("adult_count", None)
		child_count = data.get("child_count", None)
		product_id = data.get("product_id", None)
		if adult_count and child_count and product_id:
			cart = request.session.get("cart", [])
			# If cart item match the item submitted in form then delete it from cart 
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
	if not cart:
		return redirect("booking:activities") # Redirect if there are no cart items
	ctx["card_items_count"] = len(cart)
	# Calculate the total cost of all cart items
	ctx["total"] = 0
	for i in range(len(cart)):
		item = cart[i]
		cart[i]["total"] = total = item["adult_price"] * float(item["adult_count"]) + item["child_price"] * float(item["child_count"])
		ctx["total"] += total
	if request.method == "POST":
		form = UserInfoForm(request.POST)
		if form.is_valid():
			# Get form data and save it to sessions
			data = form.cleaned_data
			info = {
				"first_name":data.get("first_name"),
				"last_name":data.get("last_name"),
				"email":data.get("email"),
				"phone":data.get("phone"),
				"date":str(data.get("date").date()),
				"date_repeat":str(data.get("date_repeat").date()),
			}
			request.session["user_info"] = info
			return redirect("booking:checkout-step2")
	else:
		# Pre-populate form fields with existing user data
		initial = {}
		info = request.session.get("user_info")
		if info:
			initial = {
				"first_name": info["first_name"],
				"last_name": info["last_name"],
				"email": info["email"],
				"phone": info["phone"],
				"date": datetime.datetime.strptime(info["date"], '%Y-%m-%d').date(),
				"date_repeat": datetime.datetime.strptime(info["date_repeat"], '%Y-%m-%d').date(),
			}
		form = UserInfoForm(initial=initial)
		# Set min, max values for date inputs
		form.fields["date"].widget.attrs.update({'min': datetime.date.today() + timedelta(days=1)})
		form.fields["date_repeat"].widget.attrs.update({'min': datetime.date.today() + timedelta(days=1)})
	ctx["form"] = form
	template_file = "booking/checkout_step1.html"
	return render(request, template_file, ctx)

def checkout_step2_view(request):
	ctx = {}
	ctx["cart"] = cart = request.session.get("cart", [])
	if not cart:
		return redirect("booking:activities")
	ctx["card_items_count"] = len(cart)
	# Calculate the total cost of all cart items
	ctx["total"] = 0
	for i in range(len(cart)):
		item = cart[i]
		cart[i]["total"] = total = item["adult_price"] * float(item["adult_count"]) + item["child_price"] * float(item["child_count"])
		ctx["total"] += total
	if request.method == "POST":
		form = PaymentForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			info = request.session.get("user_info", [])
			if not info: # Make sure all user data are present
				return redirect("booking:checkout-step1")
			# Create a user profile
			profile = Profile.objects.create(
				first_name=info["first_name"],
				last_name=info["last_name"],
				email=info["email"],
				phone=info["phone"]
			)
			# Create a ticket object for every cart item
			for item in cart:
				obj = Ticket.objects.create(
					user=profile,
					activity=get_object_or_404(Activity, product_id=item["product_id"]),
					adult_count=item["adult_count"],
					child_count=item["child_count"],
					expected_activation_date=datetime.datetime.strptime(info["date"].split(' ')[0], '%Y-%m-%d'),
				)
			# Set success id in sessions
			request.session["success_id"] = profile.slug
			# Delete session data
			request.session.pop('cart', None)
			request.session.pop('user_info', None)
			# Send success email
			success_email(
				profile.email, 
				profile.get_full_name(), 
				str(len(cart)), 
				profile.slug,
				info["date"].split(" ")[0],
			)
			return redirect("booking:checkout-success")
	else:
		form = PaymentForm()
	ctx["form"] = form
	template_file = "booking/checkout_step2.html"
	return render(request, template_file, ctx)

def success_view(request, success_id=None):
	ctx = {}
	cached_success_id = request.session.get("success_id", None)
	if not (cached_success_id or success_id):
		raise Http404("Order not found")
	# Success id validation
	if cached_success_id and cached_success_id == success_id or not success_id:
		ctx["profile"] = get_object_or_404(Profile, slug=cached_success_id)
	elif request.user.is_staff:
		ctx["profile"] = get_object_or_404(Profile, slug=success_id)
	elif success_id:
		# Show email verification form if cached success id is not present or does not match the success id in url
		profile = get_object_or_404(Profile, slug=success_id)
		if request.method == "POST":
			form = UserIdentifyForm(request.POST)
			if form.is_valid():
				if form.cleaned_data.get("email") == profile.email:
					ctx["profile"] = profile
					request.session["success_id"] = success_id
				else:
					messages.add_message(request, messages.ERROR, "Order not found")
		else:
			form = UserIdentifyForm()
		ctx["form"] = form
	if "profile" in ctx:
		# Get all tickets linked to this user
		ctx["qs"] = Ticket.objects.filter(user=ctx["profile"])
	template_file = "booking/success.html"
	return render(request, template_file, ctx)


