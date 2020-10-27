from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path(
        "create/<int:product>",
        views.create,
        name="create",
    ),
    path(
        "<int:pk>/",
        views.OrderDetailView.as_view(),
        name="detail",
    ),
    path("<int:pk>/<str:verb>", views.edit_order, name="edit"),
    path("customer/", views.SeeOrdersView.as_view(), name="see-orders"),
]
