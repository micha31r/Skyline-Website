from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *

def login_view(request):
	ctx = {}
	next_page = request.GET.get("next") # Get url of the destination page
	default_page = "booking:admin-all" # Default destination page
	if request.user.is_authenticated:
		# Redirect user to the destination page if they are already logged in
		return redirect(next_page or default_page)
	login_form = LoginForm(request.POST or None)
	ctx["form"] = login_form
	if login_form.is_valid():
		# Get username and password from form
		username = login_form.cleaned_data.get("username")
		password = login_form.cleaned_data.get("password")
		# Check if username and password are correct
		user = authenticate(request, username=username, password=password)
		if user and user.is_staff: # Only login user if they are a staff member
			login(request, user)
			return redirect(next_page or default_page) # Redirect to the destination page
		else: 
			messages.add_message(request, messages.ERROR, 'Wrong username or password')
	login_form = LoginForm()
	template_file = "usermgmt/login.html"
	return render(request, template_file, ctx)

@login_required
def logout_view(request):
    logout(request)
    return redirect("usermgmt:login")