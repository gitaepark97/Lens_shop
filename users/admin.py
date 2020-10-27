from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class UserAdmin(UserAdmin):

    """ User Admin """

    fieldsets = (
        (
            "User Profile",
            {
                "fields": (
                    "username",
                    "password",
                    "email",
                    "name",
                    "avatar",
                    "gender",
                    "address",
                    "language",
                    "is_store",
                )
            },
        ),
    )

    list_filter = (
        "name",
        "language",
        "gender",
        "is_store",
    )

    list_display = (
        "username",
        "name",
        "email",
        "gender",
        "language",
        "is_store",
        "email_verified",
        "email_secret",
    )
