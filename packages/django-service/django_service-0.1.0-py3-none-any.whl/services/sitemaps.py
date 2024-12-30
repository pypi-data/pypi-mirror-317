from django.contrib import sitemaps
from django.urls import reverse
from .models import ServiceCategory, Service


class ServiceCategorySitemap(sitemaps.Sitemap):
    priority = 1
    changefreq = "yearly"

    def items(self):
        return ServiceCategory.objects.all().order_by("id")

    def location(self, item):
        return reverse("sign-detail", args=[item.slug])


class ServiceSitemap(sitemaps.Sitemap):
    priority = 1
    changefreq = "yearly"

    def items(self):
        return Service.objects.all().order_by("id")

    def location(self, item):
        return reverse("services-detail", args=[item.category.slug, item.slug])
