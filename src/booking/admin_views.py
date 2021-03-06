import datetime
from django.utils import timezone
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q, Value
from django.db.models.functions import Concat   
from usermgmt.models import Profile
from .models import Activity, Ticket

@staff_member_required
def booking_list_view(request):
	ctx = {}

	# Create new query field -> full_name
	# https://stackoverflow.com/questions/7681708/querying-full-name-in-django
	all_qs = Ticket.objects.annotate(user__full_name=Concat('user__first_name', Value(' '), 'user__last_name')).all()

	# Filter queryset
	# Store and get search parameter from session
	s = request.session
	if request.POST:
		p = request.POST
		if p.get("reset-filter", None):
			# Clear filter data session
			s["filter"] = {}
		else:
			# Save form data to session
			s["filter"] = {
				"activity": p.getlist("activity", []),
				"issue-date": p.get("issue-date", None),
				"arrival-date": p.get("arrival-date", None),
				"wildcard": p.get("wildcard", None),
				"void": p.get("void", None),
				"expired": p.get("expired", None),
				"activated": p.get("activated", None)
			}
			
	if "filter" not in s:
		s["filter"] = {}

	f = s["filter"]
	if f:
		# Get data from session
		activity = f["activity"]
		issue_date = f["issue-date"]
		arrival_date = f["arrival-date"]
		wildcard = f["wildcard"]
		void = f["void"]
		expired = f["expired"]
		activated = f["activated"]
		# If search values are set then filter the queryset
		if activity:
			all_qs = all_qs.filter(activity__product_id__in=activity)
			ctx["current_activity"] = activity
		if issue_date:
			try:
				ctx["current_issue_date"] = issue_date = datetime.datetime.strptime(issue_date, '%Y-%m-%d')
				all_qs = all_qs.filter(timestamp__date=issue_date)
			except:
				pass
		if arrival_date:
			try:
				ctx["current_arrival_date"] = arrival_date = datetime.datetime.strptime(arrival_date, '%Y-%m-%d')
				all_qs = all_qs.filter(expected_activation_date=arrival_date)
			except ValidationError:
				pass
		if wildcard:
			# Complex queries (this OR that OR those)
			lookups = Q(user__full_name__icontains=wildcard) | \
				Q(user__email__icontains=wildcard) | \
				Q(user__phone__icontains=wildcard) | \
				Q(activity__name__icontains=wildcard) | \
				Q(activity__product_id__icontains=wildcard) | \
				Q(code__icontains=wildcard)
			# Also filter by integer fields if search value is a number
			if wildcard.isdigit() and len(wildcard) < 3:
				lookups |= Q(adult_count=wildcard) | \
					Q(child_count=wildcard)
			all_qs = all_qs.filter(lookups)
			ctx["current_wildcard"] = wildcard

		# Whether to include voided, used or expired tickets
		if void: ctx["current_void"] = void
		else: all_qs = all_qs.filter(void=False)
		if expired: ctx["current_expired"] = expired
		else: all_qs = all_qs.filter(expected_activation_date__gt=timezone.now().date())
		if activated: ctx["current_activated"] = activated
		else: all_qs = all_qs.filter(activated=False)

		ctx["filter_applied"] = True
	else:
		# Hide voided, used or expired tickets if filter is not set
		all_qs = all_qs.filter(void=False, activated=False, expected_activation_date__gt=timezone.now().date())
	
	ctx["total_result_count"] = all_qs.count()

	# Get the total number of adults and children from all tickets
	total_adults = 0
	total_children = 0
	for ticket in all_qs.all():
		total_adults += ticket.adult_count
		total_children += ticket.child_count
	ctx["total_adults"] = total_adults
	ctx["total_children"] = total_children

	# Split search results in to multiple pages if needed
	paginate_by = 20
	paginator = Paginator(all_qs, paginate_by)

	current_page = request.GET.get('page', 1)
	if int(current_page) > paginator.num_pages:
		current_page = paginator.num_pages

	ctx["page_obj"] = paginator.page(current_page) # Set current page
	ctx["page_range"] = range(1, ctx["page_obj"].paginator.num_pages+1)
	ctx["activities"] = Activity.objects.all()
	template_name = 'booking/admin/booking_list.html'
	return render(request, template_name, ctx)

@staff_member_required
def booking_edit_view(request, user_slug, ticket_id):
	ctx = {}
	# Get ticket object
	ctx["obj"] = obj = get_object_or_404(Ticket, id=ticket_id, user__slug=user_slug)
	if not obj.activated and not obj.void and request.POST: # If the ticket can be edited
		# Get form data
		p = request.POST
		fn = p.get("first_name")
		ln = p.get("last_name")
		em = p.get("email")
		ph = p.get("phone")
		ad = p.get("date")
		ac = p.get("adult_count")
		cc = p.get("child_count")
		# Form validation
		if fn and ln and em and ph and ad and ac and cc:
			if not fn.isalpha():
				messages.error(request, "First name can only contain A-z and less than 65 letters")
			if not ln.isalpha():
				messages.error(request, "Last name can only contain A-z and less than 129 letters")
			phone = ph.replace("+","")
			if (len(phone) > 12 or len(phone) < 9) or not phone.isdigit():
				messages.error(request, "Phone number should be between 9-12 digits and only contain 0-9 and +")
			try:
				ad = datetime.datetime.strptime(ad, '%Y-%m-%d').date()
				if ad != obj.expected_activation_date and ad <= timezone.now().date():
					messages.error(request, "Arrival date must be a future date")
			except:
				messages.error(request, "Invalid date format, must be yyyy-mm-dd")
			try: 
				validate_email(em)
			except:
				messages.error(request, "Invalid email format")
			if not (ac.isdigit() and cc.isdigit() and int(ac) >= 0 and int(cc) >= 0):
				messages.error(request, "Number of attendees must be a positive integer")
		else:
			messages.error(request, "Invalid form data!")
		has_error = list(messages.get_messages(request))
		if not has_error:
			# Save changes if form data is valid 
			obj.user.first_name = fn
			obj.user.last_name = ln
			obj.user.email = em
			obj.user.phone = ph
			obj.user.save()
			obj.adult_count = ac
			obj.child_count = cc
			obj.expected_activation_date = ad
			obj.save()
	template_name = 'booking/admin/booking_edit.html'
	return render(request, template_name, ctx)

@staff_member_required
def booking_activate_view(request, user_slug, ticket_id):
	obj = get_object_or_404(Ticket, id=ticket_id, user__slug=user_slug)
	obj.activated = True
	obj.activation_date = timezone.now().date()
	obj.save()
	return redirect("booking:admin-all")

@staff_member_required
def booking_void_view(request, user_slug, ticket_id):
	obj = get_object_or_404(Ticket, id=ticket_id, user__slug=user_slug)
	obj.void = True
	obj.void_date = timezone.now().date()
	obj.save()
	return redirect("booking:admin-all")

    