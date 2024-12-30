from modeltranslation.translator import register, TranslationOptions
from .models import ServiceCategory, Service, ServiceImage


@register(ServiceCategory)
class ServiceCategoryTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "slug",
        "description",
    )


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "slug",
        "short_description",
        "p1_title",
        "p1",
        "p2_title",
        "p2",
        "p3_title",
        "p3",
    )


@register(ServiceImage)
class ServiceImageTranslationOptions(TranslationOptions):
    fields = (
        "description",
    )
