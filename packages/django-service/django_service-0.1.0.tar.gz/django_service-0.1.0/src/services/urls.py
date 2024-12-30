from django.urls import re_path
from .views import ServiceCategoryListView, ServiceCategoryDetailView, ServiceDetailView

urlpatterns = [
    re_path(
        r"^(?P<slug_cat>[\w-]+)/(?P<slug>[\w-]+)/$",
        ServiceDetailView.as_view(),
        name="service-detail",
    ),
    re_path(
        r"^(?P<slug_cat>[\w-]+)/$",
        ServiceCategoryDetailView.as_view(),
        name="services-category-detail",
    ),
    re_path(
        r"^services/$",
        ServiceCategoryListView.as_view(),
        name="services-categories-list",
    ),
]
