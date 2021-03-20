import datetime
from django import forms
from usermgmt.models import Profile

class UserInfoForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['first_name', 'last_name', 'email', 'phone']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name'})
		self.fields['first_name'].label = "First Name"
		self.fields['last_name'].widget.attrs.update({'placeholder': 'Last Name'})
		self.fields['last_name'].label = "Last Name"
		self.fields['email'].widget.attrs.update({'placeholder': 'example@example.com'})
		self.fields['email'].label = "Email Address"
		self.fields['phone'].widget.attrs.update({'placeholder': '(+64)(0) 12 345 6789'})
		self.fields['phone'].label = "Phone Number"

	date = forms.DateTimeField(
		widget=forms.TextInput(
	        attrs={
	            "placeholder":"Date",
	            "type": "date"
	        }
	    ),
	    label="Arrival Date"
	)
	date_repeat = forms.DateTimeField(
		widget=forms.TextInput(
	        attrs={
	            "placeholder":"Repeat Date",
	            "type": "date"
	        }
	    ),
	    label="Repeat Arrival Date"
	)

	def clean(self):
		data = super().clean()
		fn = data.get("first_name")
		ln = data.get("last_name")
		ph = data.get("phone")
		ad = data.get("date")
		rad = data.get("date_repeat")
		if fn and ln and ph and ad and rad:
			if not fn.isalpha():
				self._errors["first_name"] = ["First name can only contain A-z and less than 65 letters"]
			if not ln.isalpha():
				self._errors["last_name"] = ["Last name can only contain A-z and less than 129 letters"]
			phone = ph.replace("+","")
			if (len(phone) > 12 or len(phone) < 9) or not phone.isnumeric():
				self._errors["phone"] = ["Phone number should be between 9-12 digits and only contain 0-9 and +"]
			if ad.date() <= datetime.date.today():
				self._errors["date"] = ["Arrival date must be a future date"]
			elif ad != rad:
				self._errors["date_repeat"] = ["Arrival dates must match"]
		else:
			self._errors["first_name"] = ["Invalid form data!"]
		return data

class PaymentForm(forms.Form):
	first_name = forms.CharField(
	    widget=forms.TextInput(
	        attrs={
	            "placeholder":"First Name"
	        },
	    ),
	    label="First Name"
	)
	last_name = forms.CharField(
	    widget=forms.TextInput(
	        attrs={
	            "placeholder":"Last Name"
	        },
	    ),
	    label="Last Name"
	)
	email = forms.EmailField(
	    widget=forms.TextInput(
	        attrs={
	            "placeholder":"Email"
	        },
	    ),
	    label="Email Adress"
	)
	phone = forms.CharField(
	    widget=forms.TextInput(
	        attrs={
	            "placeholder":"Phone Number"
	        }
	    ),
	    label="Phone Number"
	)
	date = forms.DateTimeField(
		widget=forms.TextInput(
	        attrs={
	            "placeholder":"Phone Number",
	            "type": "date"
	        }
	    ),
	    label="Arrival Date"
	)
	date_repeat = forms.DateTimeField(
		widget=forms.TextInput(
	        attrs={
	            "placeholder":"Phone Number",
	            "type": "date"
	        }
	    ),
	    label="Repeat Arrival Date"
	)
