from django.db import models
from django.utils import timezone
from project.utils import slug_generator

class Profile(models.Model):
	class Meta:
		ordering = ['last_name', 'first_name', '-timestamp']

	first_name = models.CharField(max_length=64)
	last_name = models.CharField(max_length=128)
	email = models.EmailField(max_length=255)
	phone = models.CharField(max_length=13)
	slug = models.SlugField(max_length=32, blank=True, null=True)

	# Timestamp
	timestamp = models.DateTimeField(auto_now_add=True)

	def add_item(self):
		...

	def get_full_name(self):
		return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

	def save(self, *args, **kwargs):
		self.slug = slug_generator(timezone.now(), 32)
		super(Profile, self).save(*args, **kwargs)

	def __str__(self):
		return f"{self.get_full_name()} #{self.id}"
