from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
from django.db.models import Q
from usermgmt.models import Profile
from .models import Activity, Ticket

@login_required
def booking_list_view(request):
	if not request.user.is_staff:
		return Http404()

	ctx = {}
	all_qs = Ticket.objects.all()
	# Filter queryset
	# Store and get search parameter from session
	s = request.session
	if request.POST:
		p = request.POST
		s["activity"] = p.getlist("activity")
		s["issue-date"] = p.get("issue-date")
		s["arrival-date"] = p.get("arrival-date")
		s["wildcard"] = p.get("wildcard")
	activity = s.get("activity", [])
	issue_date = s.get("issue-date", None)
	arrival_date = s.get("arrival-date", None)
	wildcard = s.get("wildcard", None)
	if activity:
		all_qs = all_qs.filter(activity__product_id__in=activity)
	if issue_date:
		all_qs = all_qs.filter(timestamp=issue_date)
	if arrival_date:
		all_qs = all_qs.filter(activation_date=arrival_date)
	if wildcard:
		lookups = Q(user__first_name__icontains=wildcard) | \
			Q(user__last_name__icontains=wildcard) | \
			Q(activity__name__icontains=wildcard) | \
			Q(activity__product_id=wildcard) | \
			Q(code=wildcard)
		if wildcard.isdigit() and len(wildcard) < 3:
			lookups |= Q(adult_count=wildcard) | \
				Q(child_count=wildcard)
		all_qs = all_qs.filter(lookups)
	ctx["total_result_count"] = all_qs.count()

	paginate_by = 30
	paginator = Paginator(all_qs, paginate_by)
	ctx["page_obj"] = paginator.page(request.GET.get('page', 1)) # Set current page
	ctx["page_range"] = range(1, ctx["page_obj"].paginator.num_pages+1)
	ctx["activities"] = Activity.objects.all()
	template_name = 'booking/admin/booking_list.html'
	return render(request, template_name, ctx)
    