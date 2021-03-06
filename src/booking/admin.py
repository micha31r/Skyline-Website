from django.contrib import admin
from .models import Activity, Ticket

class ActivityAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'product_id', 'adult_price', 'child_price', 'pk')
	search_fields = ('name', 'product_id', 'adult_price', 'child_price')

class TicketAdmin(admin.ModelAdmin):
	list_display = ('user', 'activity', 'expected_activation_date', 'activated', 'void', 'timestamp', 'pk')
	search_fields = ('user', 'activity__product_id', 'expiry_date')
	readonly_fields = ["code", "timestamp"]

admin.site.register(Activity, ActivityAdmin)
admin.site.register(Ticket, TicketAdmin)

