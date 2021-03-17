from django.shortcuts import render
from django.views.generic.base import TemplateView

class HomeView(TemplateView):
    template_name = "home.html"

def handler404(request, exception=None):
	return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)