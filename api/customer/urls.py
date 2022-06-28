from django.urls import path, include


app_name = "owner"

urlpatterns = [
    path("<int:owner>/", include("api.customer.owner.urls", namespace="owner")),
]
