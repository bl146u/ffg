from django.urls import path

from . import views


app_name = "owner"

urlpatterns = [
    path("checks-list/", views.ChecksListAPIView.as_view(), name="checks_list"),
    path("products-list/", views.ProductsListAPIView.as_view(), name="products_list"),
    path("shops-list/", views.ShopsListAPIView.as_view(), name="shops_list"),
]
