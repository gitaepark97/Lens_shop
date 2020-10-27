from django.contrib import messages
from django.shortcuts import redirect, reverse
from products import models as product_models
from . import forms


def create_review(request, product):
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        product = product_models.Product.objects.get_or_none(pk=product)
        if not product:
            return redirect(reverse("core:home"))
        if form.is_valid():
            review = form.save()
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Product reviewed")
            return redirect(reverse("products:detail", kwargs={"pk": product.pk}))
