from django.urls import path, include


app_name = "api"

urlpatterns = [
    path("customer/", include("api.customer.urls", namespace="customer")),
    path("checks/", include("api.checks.urls", namespace="checks")),
]
