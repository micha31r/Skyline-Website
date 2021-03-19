from django.shortcuts import render
from .models import Activity

def activities_view(request):
	ctx = {}
	ctx["qs"] = Activity.objects.all().order_by("child_price")
	template_file = "booking/activities.html"
	return render(request, template_file, ctx)