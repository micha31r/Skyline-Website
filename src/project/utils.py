import datetime, os, string, random
from django.utils import timezone

def slug_generator(seed, size=6, chars=string.ascii_letters + string.digits):
    random.seed(seed)
    return ''.join(random.choice(chars) for _ in range(size))

# Return 1 to 7 based on the day
def day_in_week(date):
	return (int(date.strftime("%w"))-1)%7+1

# Return the current week 
def current_week():
	return int(timezone.now().date().strftime('%W'))

def current_day():
    return int(timezone.now().date().strftime('%d'))

def current_month():
    return int(timezone.now().date().strftime('%m'))

def current_year():
    return int(timezone.now().date().strftime('%Y'))

# Date class
class Date:
    def now(self):
        return timezone.now().date()

    def week(self):
        return current_week()

    def day(self):
        return current_day()

    def month(self):
        return current_month()

    def year(self):
        return current_year()