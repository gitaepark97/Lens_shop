from django.contrib import admin
from . import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):

    """ Order Admin Definition """

    list_display = ("product",)

    list_filter = ("product",)
