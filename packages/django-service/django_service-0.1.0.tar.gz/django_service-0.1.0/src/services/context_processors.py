# -*- coding: utf-8 -*-
"""
Context processors for services app
"""

from django.core.cache import cache
from django.contrib import messages
from filer_optimizer.utils import annotate_queryset_with_thumbnails

from .models import ServiceCategory, Service


def common_context(request):
    """Returns the common info for all services components (Could be used by menu, footer, etc.)"""

    cache_key = "services_common_context"
    context_cache = None
    try:
        context_cache = cache.get(cache_key)
    except Exception as err:
        context_cache = None

    if context_cache is None:
        try:
            queryset = Service.objects.filter(published=True).values('category__order', 'category__name', 'category__slug', 'name', 'slug', 'short_description').order_by('category__order', 'order')
            queryset = annotate_queryset_with_thumbnails(queryset, "grid", img_name="image_preview")

            context = {
                'all_category': ServiceCategory.objects.filter(published=True).values('name', 'slug').order_by('order'),
                'all_service': queryset,
            }
            context_cache = cache.set(cache_key, context, timeout=86400)
            return context
        except Exception as err:
            messages.error(request, err)
    return context_cache
