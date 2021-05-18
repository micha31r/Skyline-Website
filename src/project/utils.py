import datetime, os, string, random
from django.utils import timezone

# Generates a random string
def slug_generator(seed, size=6, chars=string.ascii_letters + string.digits):
    random.seed(seed)
    return ''.join(random.choice(chars) for _ in range(size))
