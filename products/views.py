from django.http import Http404
from django.views.generic import (
    ListView,
    DetailView,
    View,
    UpdateView,
    FormView,
)
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from users import mixins as user_mixins
from orders import models as order_models
from . import models, forms


class RecommendView(View):

    """ RecommendView Definition """

    def get(self, request):

        products = models.Product.objects.all()
        orders = order_models.Order.objects.filter(user=request.user)

        recommends = set()

        for order in orders:
            for product in products:
                if product.color_type == order.product.color_type:
                    if product != order.product:
                        recommends.add(product)

        qs = list(recommends)

        paginator = Paginator(qs, 8, orphans=3)

        page = request.GET.get("page", 1)

        products = paginator.get_page(page)

        return render(
            request,
            "products/recommend_list.html",
            {"products": products},
        )


class HomeView(ListView):

    """ HomeView Definition """

    template_name = "index.html"
    model = models.Product
    paginate_by = 8
    paginate_orphans = 3
    ordering = "created"
    context_object_name = "products"


class ProductDetail(DetailView):

    """ ProductDetail Definition """

    model = models.Product


class SearchView(View):
    def get(self, request):

        form = forms.SearchForm(request.GET)

        if form.is_valid():

            name = form.cleaned_data.get("name")
            color_type = form.cleaned_data.get("color_type")
            cycle = form.cleaned_data.get("cycle")
            size = form.cleaned_data.get("size")
            lens_type = form.cleaned_data.get("lens_type")
            company = form.cleaned_data.get("company")
            price = form.cleaned_data.get("price")

            filter_args = {}

            if name != "Anything":
                filter_args["name__startswith"] = name

            if company is not None:
                filter_args["company"] = company

            if color_type is not None:
                filter_args["color_type"] = color_type

            if cycle is not None:
                filter_args["cycle"] = cycle

            if size is not None:
                filter_args["size__lte"] = size

            if lens_type is not None:
                filter_args["lens_type"] = lens_type

            if price is not None:
                filter_args["price__lte"] = price

            qs = models.Product.objects.filter(**filter_args).order_by("-created")

            paginator = Paginator(qs, 8, orphans=3)

            page = request.GET.get("page", 1)

            products = paginator.get_page(page)

        return render(
            request,
            "products/search.html",
            {"form": form, "products": products},
        )


class EditProductView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Product
    template_name = "products/product_edit.html"
    fields = (
        "name",
        "description",
        "price",
        "color_type",
        "lens_type",
        "cycle",
        "company",
        "powers",
    )

    def get_object(self, queryset=None):
        product = super().get_object(queryset=queryset)
        if product.store.pk != self.request.user.pk:
            raise Http404()
        return product


class ProductPhotosView(user_mixins.LoggedInOnlyView, ProductDetail):

    model = models.Product
    template_name = "products/product_photos.html"

    def get_object(self, queryset=None):
        product = super().get_object(queryset=queryset)
        if product.store.pk != self.request.user.pk:
            raise Http404()
        return product


@login_required
def delete_product(request, pk):
    user = request.user
    try:
        product = models.Product.objects.get(pk=pk)
        if product.store.pk != user.pk:
            messages.error(request, "Can't delete that product")
        else:
            models.Product.objects.filter(pk=pk).delete()
            messages.success(request, "Product Deleted!")
        return redirect(reverse("users:profile", kwargs={"pk": product.store.pk}))
    except models.Product.DoesNotExist:
        return redirect(reverse("core:home"))


@login_required
def delete_photo(request, product_pk, photo_pk):
    user = request.user
    try:
        product = models.Product.objects.get(pk=product_pk)
        if product.store.pk != user.pk:
            messages.error(request, "Can't delete that photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Deleted!")
        return redirect(reverse("products:photos", kwargs={"pk": product_pk}))
    except models.Product.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "products/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    success_message = "Photo Updated"
    fields = ("caption",)

    def get_success_url(self):

        product_pk = self.kwargs.get("product_pk")
        return reverse("products:photos", kwargs={"pk": product_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, FormView):

    model = models.Photo
    template_name = "products/photo_create.html"
    fields = (
        "caption",
        "file",
    )
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("products:photos", kwargs={"pk": pk}))


class CreateProductView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateProductForm
    template_name = "products/product_create.html"

    def form_valid(self, form):
        product = form.save()
        product.store = self.request.user
        product.save()
        messages.success(self.request, "Product Created")
        return redirect(reverse("products:detail", kwargs={"pk": product.pk}))
