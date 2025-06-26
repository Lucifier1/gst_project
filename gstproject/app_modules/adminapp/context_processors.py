
from app_modules.adminapp import models
from django.core.cache import cache


def global_data(request):
    cache_key = 'global_data_key'
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        try:
            basic_details = models.BasicDetails.objects.first()
        except:
            basic_details = None

        context = {
            'basic_details': basic_details if basic_details else None,
        }
        cache.set(cache_key, context, timeout=300) 
    else:
        context = cached_data
    return context