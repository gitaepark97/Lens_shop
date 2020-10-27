from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.ColorType, models.LensType, models.Cycle, models.Company)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.products.count()

    pass


class PhotoInline(admin.TabularInline):

    model = models.Photo


@admin.register(models.Power)
class PowerAdmin(admin.ModelAdmin):

    """ Power Admin Definition """

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "sph",
                    "cyl",
                    "stock",
                )
            },
        ),
    )

    list_display = ("__str__",)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):

    """ Product Admin Definition """

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "description",
                    "color_type",
                    "price",
                    "lens_type",
                )
            },
        ),
        (
            "More About",
            {"fields": ("cycle", "size", "detail_color", "company", "powers")},
        ),
        ("Last Details", {"fields": ("store",)}),
    )

    list_display = (
        "name",
        "price",
        "color_type",
        "cycle",
        "GDIA",
        "lens_type",
        "company",
        "count_photos",
        "total_rating",
    )
    list_filter = (
        "lens_type",
        "company",
        "color_type",
    )

    filter_horizontal = ("powers",)

    raw_id_fields = ("store",)

    search_fields = ("^name", "^store__name")

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Phot Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"
