import datetime, os, string, random
from django.utils import timezone

def slug_generator(seed, size=6, chars=string.ascii_letters + string.digits):
    random.seed(seed)
    return ''.join(random.choice(chars) for _ in range(size))
