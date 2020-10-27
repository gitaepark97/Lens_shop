from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.generic import View
from django.shortcuts import render, redirect, reverse
from products import models as product_models
from reviews import forms as review_forms
from . import models


class CreateError(Exception):
    pass


@login_required
def create(request, product):
    try:
        product = product_models.Product.objects.get(pk=product)
        user = request.user
        order = models.Order.objects.get(user=user, product=product)
        return redirect(reverse("orders:detail", kwargs={"pk": order.pk}))
    except models.Order.DoesNotExist:
        order = models.Order.objects.create(user=user, product=product)
        return redirect(reverse("orders:detail", kwargs={"pk": order.pk}))


class OrderDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        order = models.Order.objects.get_or_none(pk=pk)
        if not order or (
            order.user != self.request.user and order.product.store != self.request.user
        ):
            raise Http404()
        form = review_forms.CreateReviewForm()
        return render(
            self.request,
            "orders/detail.html",
            {"order": order, "form": form},
        )


def edit_order(request, pk, verb):
    order = models.Order.objects.get_or_none(pk=pk)
    if not order or (
        order.user != request.user and order.product.store != request.user
    ):
        raise Http404()
    if verb == "confirm":
        order.status = models.Order.STATUS_CONFIRMED
        order.save()
        return redirect(reverse("orders:detail", kwargs={"pk": order.pk}))
    elif verb == "cancel":
        order.status = models.Order.STATUS_CANCELED
        messages.success(request, "Order Canceled")
        order.save()
        models.Order.objects.filter(status=models.Order.STATUS_CANCELED).delete()
        return redirect(reverse("products:detail", kwargs={"pk": order.product.pk}))


class SeeOrdersView(TemplateView):

    template_name = "orders/order_show.html"
