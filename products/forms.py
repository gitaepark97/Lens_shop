from django import forms
from . import models


class SearchForm(forms.Form):

    name = forms.CharField(required=False, initial="Anything")
    color_type = forms.ModelChoiceField(
        required=False, empty_label="Any kind", queryset=models.ColorType.objects.all()
    )
    cycle = forms.ModelChoiceField(
        required=False, empty_label="Any kind", queryset=models.Cycle.objects.all()
    )
    lens_type = forms.ModelChoiceField(
        required=False, empty_label="Any kind", queryset=models.LensType.objects.all()
    )
    company = forms.ModelChoiceField(
        required=False, empty_label="Any kind", queryset=models.Company.objects.all()
    )
    size = forms.FloatField(required=False)
    price = forms.IntegerField(required=False)


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ("caption", "file")

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        product = models.Product.objects.get(pk=pk)
        photo.product = product
        photo.save()


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = (
            "name",
            "description",
            "price",
            "size",
            "color_type",
            "lens_type",
            "cycle",
            "company",
            "powers",
        )

    def save(self, *args, **kwargs):
        product = super().save(commit=False)
        return product
