from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from ordered_model.admin import OrderedModelAdmin
from model_mixin.admin import ModelAdminAuditFieldsMixin, ModelAdminPublishFieldsMixin
from .models import ServiceCategory, Service, ServiceImage


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(
    TranslationAdmin,
    ModelAdminAuditFieldsMixin,
    ModelAdminPublishFieldsMixin,
    OrderedModelAdmin,
):

    actions = ["make_published"]

    list_display = [
        "published",
        "order",
        "move_up_down_links",
        "name",
        "modified",
        "modified_by",
    ]
    list_display_links = ["name"]
    list_filter = ("name",)
    prepopulated_fields = {"slug": ["name"]}
    ordering = ("order",)
    readonly_fields = (
        "move_up_down_links",
        "publish",
        "publish_by",
        "created",
        "created_by",
        "modified",
        "modified_by",
    )


class ServiceImageInline(TranslationTabularInline):
    model = ServiceImage


@admin.register(Service)
class ServiceAdmin(
    TranslationAdmin,
    ModelAdminAuditFieldsMixin,
    ModelAdminPublishFieldsMixin,
    OrderedModelAdmin,
):
    list_display = [
        "published",
        "order",
        "move_up_down_links",
        "category",
        "name",
        "modified",
        "modified_by",
    ]
    list_display_links = ["name"]
    list_filter = ("category",)
    prepopulated_fields = {"slug": ["name"]}
    search_fields = ["name", "category__name"]
    ordering = (
        "category",
        "order",
    )
    readonly_fields = (
        "move_up_down_links",
        "publish",
        "publish_by",
        "created",
        "created_by",
        "modified",
        "modified_by",
    )
    inlines = [
        ServiceImageInline,
    ]