from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from core import models as core_models


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ColorType(AbstractItem):

    """ ColorType Model Definition """

    class Meta:
        verbose_name = "Color Type"


class Cycle(AbstractItem):

    """ Cycle Model Definition """

    class Meta:
        verbose_name_plural = "Cycles"


class Company(AbstractItem):

    """ Company Model Definition """

    pass

    class Meta:
        verbose_name_plural = "Companies"


class LensType(AbstractItem):

    """ LensType Model Definition """

    class Meta:
        verbose_name = "Lens Type"


class Power(core_models.TimeStampedModel):

    """ LensType Model Definition """

    sph = models.FloatField(max_length=30, default=0)
    cyl = models.FloatField(max_length=30, default=0)
    stock = models.BooleanField(default=False)

    def __str__(self):
        SPH = format(self.sph, ".2f")
        CYL = format(self.cyl, ".2f")
        return "CPH:{} CYL:{} Stock:{}".format(SPH, CYL, self.stock)

    class Meta:
        verbose_name = "Power"


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="product_photos", blank=True)
    product = models.ForeignKey(
        "Product", related_name="photos", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.caption


class Product(core_models.TimeStampedModel):

    """ Product Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    company = models.ForeignKey(
        "Company", related_name="products", on_delete=models.SET_NULL, null=True
    )
    price = models.IntegerField()
    size = models.FloatField()
    detail_color = models.CharField(max_length=50, blank=True, null=True)
    store = models.ForeignKey(
        "users.User", related_name="products", on_delete=models.CASCADE
    )
    color_type = models.ForeignKey(
        "ColorType", related_name="products", on_delete=models.SET_NULL, null=True
    )
    cycle = models.ForeignKey(
        "Cycle", related_name="products", on_delete=models.SET_NULL, null=True
    )
    lens_type = models.ForeignKey(
        "LensType", related_name="products", on_delete=models.SET_NULL, null=True
    )
    powers = models.ManyToManyField("Power", related_name="products", blank=True)

    def GDIA(self):
        GDIA = format(self.size, ".1f")
        return GDIA

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews), 2)
        return 0

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos
