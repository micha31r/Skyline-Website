import uuid
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from project.utils import slug_generator

# Activity table
class Activity(models.Model):
	class Meta:
		ordering = ['name', 'product_id', 'adult_price', 'child_price']

	name = models.CharField(max_length=128)
	adult_price = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(500)])
	child_price = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(500)])
	description = models.CharField(max_length=255)
	product_id = models.CharField(max_length=16, unique=True)

	def __str__(self):
		return f"{self.name} / {self.product_id}"

# Ticket table
class Ticket(models.Model):
	class Meta:
		ordering = ['-pk', 'expected_activation_date']

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

	expected_activation_date = models.DateField()
	activation_date = models.DateField(blank=True, null=True)
	activated = models.BooleanField(default=False)
	void_date = models.DateField(blank=True, null=True)
	void = models.BooleanField(default=False)
	code = models.UUIDField(default=uuid.uuid1, editable=False, unique=True)

	# Timestamp
	timestamp = models.DateTimeField(auto_now_add=True)

	def has_expired(self):
		if timezone.now().date() > self.expected_activation_date:
			return True
		return False

	def __str__(self):
		return f"{self.activity} #{self.id}"
