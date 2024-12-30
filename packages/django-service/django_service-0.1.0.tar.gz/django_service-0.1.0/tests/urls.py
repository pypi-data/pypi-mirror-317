"""Test's urls view for django-services"""

from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path, re_path
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path("", include("services.urls")),
]

urlpatterns += i18n_patterns(
    re_path(r"^jsi18n/$", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("", include("services.urls")),
)
