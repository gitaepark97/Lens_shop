from django.urls import path
from products import views as product_views
from users import views as user_views

app_name = "core"

urlpatterns = [
    path("", product_views.HomeView.as_view(), name="home"),
    path("recommends/", product_views.RecommendView.as_view(), name="recommends"),
    path("shops/", user_views.ShopView.as_view(), name="shops"),
]
