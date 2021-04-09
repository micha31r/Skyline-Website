from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from usermgmt.models import Profile
from .models import Activity, Ticket

@method_decorator(login_required, name='dispatch')
class BookingListView(ListView):
	model = Ticket
	paginate_by = 10
	template_name = 'booking/admin/booking_list.html'

	def dispatch(self, request, *args, **kwargs):
		if self.request.user.is_staff:
			return super().dispatch(request, *args, **kwargs)
		else: return Http404()

	def get_context_data(self, **kwargs):
		ctx = super(BookingListView, self).get_context_data(**kwargs)
		qs = list(ctx["object_list"])
		# ctx["total"] = 0
		for i in range(len(qs)):
			item = qs[i]
			total = item.activity.adult_price * float(item.adult_count) + item.activity.child_price * float(item.child_count)
			qs[i].total = total
			# ctx["total"] += total
		return ctx

    