from django.db import models
from django.utils.translation import gettext_lazy as _
from django_prose_editor.fields import ProseEditorField
from ordered_model.models import OrderedModel
from model_mixin.models import AuditModelMixin, PublishModelMixin
from filer.fields.image import FilerImageField
from taggit.managers import TaggableManager
from hashtag.models import MyTaggedItem


class ServiceCategory(AuditModelMixin, PublishModelMixin, OrderedModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=False, unique=True)
    description = models.CharField(max_length=200, blank=True)

    image_header = FilerImageField(verbose_name=_("Image Header"), null=True, blank=True, on_delete=models.CASCADE, related_name='category_image_header')
    image_preview = FilerImageField(verbose_name=_("Image Preview"), null=True, blank=True, on_delete=models.CASCADE, related_name='category_image_preview')

    class Meta:
        verbose_name = _("Service's Category")
        verbose_name_plural = _("Service's Categories")
        ordering = ("order",)

    def __str__(self):
        return self.name


class Service(AuditModelMixin, PublishModelMixin, OrderedModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=False, unique=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)

    tags = TaggableManager(through=MyTaggedItem, blank=True)

    short_description = ProseEditorField(
        verbose_name=_("Short Description"), max_length=350, null=True, blank=True
    )

    p1_title = models.CharField("(1) "+_("Paragraph's Title"), max_length=200, null=True, blank=True)
    p1 = ProseEditorField(
        verbose_name="(1) "+_("Paragraph"), max_length=5000, null=True, blank=True
    )
    p2_title = models.CharField("(2) "+_("Paragraph's Title"), max_length=200, null=True, blank=True)
    p2 = ProseEditorField(
        verbose_name="(2) "+_("Paragraph"), max_length=5000, null=True, blank=True
    )
    p3_title = models.CharField("(3) "+_("Paragraph's Title"), max_length=200, null=True, blank=True)
    p3 = ProseEditorField(
        verbose_name="(3) "+_("Paragraph"), max_length=5000, null=True, blank=True
    )

    image_header = FilerImageField(verbose_name=_("Image Header"), null=True, blank=True, on_delete=models.CASCADE, related_name='service_image_header')
    image_preview = FilerImageField(verbose_name=_("Image Preview"), null=True, blank=True, on_delete=models.CASCADE, related_name='service_image_preview')

    order_with_respect_to = "category"

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = (
            "category",
            "order",
        )

    def __str__(self):
        return self.name


class ServiceImage(models.Model):
    image = FilerImageField(verbose_name=_("Image"), on_delete=models.CASCADE)
    obj = models.ForeignKey(Service, on_delete=models.CASCADE)

    highlighted = models.BooleanField(verbose_name=_("Highlighted"), default=False)

    place = models.CharField(_("Place"), null=True, blank=True, max_length=30)
    description = models.CharField(_("Description"), null=True, blank=True, max_length=60)

    def __str__(self):
        return self.image.original_filename