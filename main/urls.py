from django.urls import path
from .views import shorten_url_view, redirect_to_original, url_stats

urlpatterns = [
    path('', shorten_url_view, name='shorten-url'),
    path('<str:short_code>/', redirect_to_original, name='redirect-to-original'),
    path('stats/<str:short_code>/', url_stats, name='url_stats'),

]
