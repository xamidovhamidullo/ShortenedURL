from django.contrib import admin
from .models import ShortenedURL, URLVisit


admin.site.register(ShortenedURL)
admin.site.register(URLVisit)