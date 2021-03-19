from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'phone', 'email', 'timestamp', 'pk')
	search_fields = ('last_name', 'first_name', 'email', 'phone')
	readonly_fields = ["timestamp"]

admin.site.register(Profile, ProfileAdmin)

