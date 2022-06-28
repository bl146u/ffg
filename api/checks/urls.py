from django.urls import path

from . import views


app_name = "checks"

urlpatterns = [
    path("cost/", views.CostAPIView.as_view(), name="cost"),
    path("list/", views.ListAPIView.as_view(), name="list"),
    path("import/", views.ImportAPIView.as_view(), name="import"),
]
