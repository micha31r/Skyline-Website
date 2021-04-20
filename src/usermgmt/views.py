from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *

def login_view(request):
	ctx = {} # Context variables
	next_page = request.GET.get("next") # Get url of the next page
	default_page = "booking:admin-all"
	if request.user.is_authenticated:
		return redirect(next_page or default_page)
	login_form = LoginForm(request.POST or None)
	ctx["form"] = login_form
	if login_form.is_valid():
		username = login_form.cleaned_data.get("username")
		password = login_form.cleaned_data.get("password")
		user = authenticate(request, username=username, password=password)
		if user and user.is_staff:
			login(request, user)
			return redirect(next_page or default_page) # Redirect to the next page
		else: 
			messages.add_message(request, messages.ERROR, 'Wrong username or password')
	login_form = LoginForm()
	template_file = "usermgmt/login.html"
	return render(request, template_file, ctx)

@login_required
def logout_view(request):
    logout(request)
    return redirect("usermgmt:login")