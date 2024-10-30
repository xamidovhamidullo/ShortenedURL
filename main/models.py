import random
import string
from django.db import models
from django.utils import timezone


class ShortenedURL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=6, unique=True, blank=True)
    visit_count = models.PositiveIntegerField(default=0)  # Tashriflar soni

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self.generate_unique_short_code()
        super().save(*args, **kwargs)

    def generate_unique_short_code(self):
        characters = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choice(characters) for _ in range(6))
            if not ShortenedURL.objects.filter(short_code=short_code).exists():
                return short_code

    def __str__(self):
        return f"{self.original_url} -> {self.short_code}"


class URLVisit(models.Model):
    url = models.ForeignKey(ShortenedURL, related_name='visits', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.ip_address} visited {self.url.short_code} at {self.timestamp}"