from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView

from django.db.models import Sum

from api import mixins_views, serializers

from shops import models as shops_models

from . import filters


class CostAPIView(mixins_views.SuperuserAPIViewMixin, ListAPIView):
    """
    Сумма покупок в интервале дат.
    """

    filter_backends = [filters.DateRangeFilter]
    queryset = shops_models.PaymentCheckModel.objects

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = queryset.values_list("cost", flat=True).aggregate(cost=Sum("cost"))
        if not response.get("cost"):
            response.update({"cost": 0})
        return Response(response)


class ListAPIView(mixins_views.SuperuserAPIViewMixin, ListAPIView):
    """
    Список чеков с товарами в интервале дат или на конкретную дату.
    """

    serializer_class = serializers.CheckCustomerSerializer
    filter_backends = [filters.DateRangeOneFilter]
    queryset = shops_models.PaymentCheckModel.objects.select_related(
        "customer", "shop"
    ).prefetch_related("product_checks", "product_checks__product")


class ImportAPIView(mixins_views.SuperuserAPIViewMixin, CreateAPIView):
    """
    Загрузка чеков в формате JSON.
    """

    serializer_class = serializers.ImportChecksSerializer
