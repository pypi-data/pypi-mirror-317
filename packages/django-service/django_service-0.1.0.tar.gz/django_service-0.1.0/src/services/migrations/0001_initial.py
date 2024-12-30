from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("hashtag", "0004_alter_mytaggeditem_content_type_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Service",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Modified"
                    ),
                ),
                (
                    "publish",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Published"
                    ),
                ),
                (
                    "published",
                    models.BooleanField(default=False, verbose_name="Publish"),
                ),
                (
                    "order",
                    models.PositiveIntegerField(
                        db_index=True, editable=False, verbose_name="order"
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("slug", models.SlugField(unique=True)),
                (
                    "short_description",
                    models.TextField(
                        blank=True,
                        max_length=350,
                        null=True,
                        verbose_name="Short Description",
                    ),
                ),
                (
                    "p1_title",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name="(1) Paragraph's Title",
                    ),
                ),
                (
                    "p1",
                    models.TextField(
                        blank=True,
                        max_length=5000,
                        null=True,
                        verbose_name="(1) Paragraph",
                    ),
                ),
                (
                    "p2_title",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name="(2) Paragraph's Title",
                    ),
                ),
                (
                    "p2",
                    models.TextField(
                        blank=True,
                        max_length=5000,
                        null=True,
                        verbose_name="(2) Paragraph",
                    ),
                ),
                (
                    "p3_title",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name="(3) Paragraph's Title",
                    ),
                ),
                (
                    "p3",
                    models.TextField(
                        blank=True,
                        max_length=5000,
                        null=True,
                        verbose_name="(3) Paragraph",
                    ),
                ),
            ],
            options={
                "verbose_name": "Service",
                "verbose_name_plural": "Services",
                "ordering": ("category", "order"),
            },
        ),
        migrations.CreateModel(
            name="ServiceImage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "highlighted",
                    models.BooleanField(default=False, verbose_name="Highlighted"),
                ),
                (
                    "place",
                    models.CharField(
                        blank=True, max_length=30, null=True, verbose_name="Place"
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True, max_length=60, null=True, verbose_name="Description"
                    ),
                ),
                (
                    "image",
                    filer.fields.image.FilerImageField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.FILER_IMAGE_MODEL,
                        verbose_name="Image",
                    ),
                ),
                (
                    "obj",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="services.service",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ServiceCategory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Modified"
                    ),
                ),
                (
                    "publish",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Published"
                    ),
                ),
                (
                    "published",
                    models.BooleanField(default=False, verbose_name="Publish"),
                ),
                (
                    "order",
                    models.PositiveIntegerField(
                        db_index=True, editable=False, verbose_name="order"
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("slug", models.SlugField(unique=True)),
                ("description", models.CharField(blank=True, max_length=200)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "image_header",
                    filer.fields.image.FilerImageField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="category_image_header",
                        to=settings.FILER_IMAGE_MODEL,
                        verbose_name="Image Header",
                    ),
                ),
                (
                    "image_preview",
                    filer.fields.image.FilerImageField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="category_image_preview",
                        to=settings.FILER_IMAGE_MODEL,
                        verbose_name="Image Preview",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_modified_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Modified By",
                    ),
                ),
                (
                    "publish_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_publish_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Published By",
                    ),
                ),
            ],
            options={
                "verbose_name": "Service's Category",
                "verbose_name_plural": "Service's Categories",
                "ordering": ("order",),
            },
        ),
        migrations.AddField(
            model_name="service",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="services.servicecategory",
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_created_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="image_header",
            field=filer.fields.image.FilerImageField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="service_image_header",
                to=settings.FILER_IMAGE_MODEL,
                verbose_name="Image Header",
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="image_preview",
            field=filer.fields.image.FilerImageField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="service_image_preview",
                to=settings.FILER_IMAGE_MODEL,
                verbose_name="Image Preview",
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="modified_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_modified_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Modified By",
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="publish_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_publish_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Published By",
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="tags",
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="hashtag.MyTaggedItem",
                to="hashtag.MyTag",
                verbose_name="Tags",
            ),
        ),
    ]
