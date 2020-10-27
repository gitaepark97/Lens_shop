from django.db import models
from core import models as core_models


class Order(core_models.TimeStampedModel):

    """ Order Model Definition """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    product = models.ForeignKey(
        "products.Product", related_name="orders", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "users.User", related_name="orders", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} - {self.product}"
