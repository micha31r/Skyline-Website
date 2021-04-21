import string, uuid
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from project.utils import slug_generator

class Activity(models.Model):
	class Meta:
		ordering = ['name', 'product_id', 'adult_price', 'child_price']

	name = models.CharField(max_length=128)
	adult_price = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(500)])
	child_price = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(500)])
	description = models.CharField(max_length=255)
	product_id = models.CharField(max_length=16)

	def __str__(self):
		return f"{self.name} / {self.product_id}"

class Ticket(models.Model):
	class Meta:
		ordering = ['-timestamp', 'activation_date']

	user = models.ForeignKey(
		"usermgmt.Profile",
		related_name="ticket_profile",
		on_delete = models.CASCADE,
	)

	activity = models.ForeignKey(
		Activity,
		related_name="ticket_activity",
		on_delete = models.CASCADE,
	)

	adult_count = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)])
	child_count = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)])

	activation_date = models.DateTimeField()
	activated = models.BooleanField(default=False)
	void = models.BooleanField(default=False)
	code = models.SlugField(max_length=32, blank=True, null=True, unique=True)

	# Timestamp
	timestamp = models.DateTimeField(auto_now_add=True)

	def has_expired(self):
		if timezone.now() > self.activation_date:
			return True
		return False

	def save(self, *args, **kwargs):
		if not self.code:
			# self.code = slug_generator(timezone.now(), 32, string.digits)
			self.code = uuid.uuid1().hex
		super(Ticket, self).save(*args, **kwargs)

	def __str__(self):
		return f"{self.activity} #{self.id}"
