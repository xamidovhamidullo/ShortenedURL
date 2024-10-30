from django.shortcuts import render, get_object_or_404, redirect
from .models import ShortenedURL, URLVisit
from .forms import URLForm
from django.http import HttpResponse


def shorten_url_view(request):
    form = URLForm(request.POST or None)
    short_url = None

    if request.method == "POST" and form.is_valid():
        instance, created = ShortenedURL.objects.get_or_create(
            original_url=form.cleaned_data['original_url']
        )
        short_url = request.build_absolute_uri('/') + instance.short_code

    return render(request, 'shorten_url.html', {'form': form, 'short_url': short_url})


def get_client_ip(request):
    """Foydalanuvchi IP-manzilini olish."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def redirect_to_original(request, short_code):
    url_instance = get_object_or_404(ShortenedURL, short_code=short_code)
    client_ip = get_client_ip(request)

    if not URLVisit.objects.filter(url=url_instance, ip_address=client_ip).exists():
        URLVisit.objects.create(url=url_instance, ip_address=client_ip)
        url_instance.visit_count += 1
        url_instance.save()

    return redirect(url_instance.original_url)


def url_stats(request, short_code):
    url_instance = get_object_or_404(ShortenedURL, short_code=short_code)
    visits = URLVisit.objects.filter(url=url_instance)
    context = {
        'original_url': url_instance.original_url,
        'short_code': url_instance.short_code,
        'visit_count': url_instance.visit_count,
    }
    return render(request, 'url_stats.html', context)