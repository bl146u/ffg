from rest_framework.generics import ListAPIView

from api import mixins_views, serializers

from shops import models as shops_models


class ChecksListAPIView(mixins_views.CustomerOwnedAPIViewMixin, ListAPIView):
    """
    Список чеков, выданных одному клиенту.
    """

    serializer_class = serializers.CheckSerializer
    queryset = shops_models.PaymentCheckModel.objects.select_related(
        "shop"
    ).prefetch_related("product_checks", "product_checks__product")

    def get_queryset(self):
        return super().get_queryset().filter(customer=self.owner)


class ProductsListAPIView(mixins_views.CustomerOwnedAPIViewMixin, ListAPIView):
    """
    Список товаров, купленных одним клиентом.
    """

    serializer_class = serializers.ProductChecksShopSerializer
    queryset = shops_models.ProductCheckModel.objects.select_related(
        "product", "product__shop", "payment_check"
    )

    def get_queryset(self):
        return super().get_queryset().filter(payment_check__customer=self.owner)


class ShopsListAPIView(mixins_views.CustomerOwnedAPIViewMixin, ListAPIView):
    """
    Список магазинов одного клиента.
    """

    serializer_class = serializers.ShopSerializer
    queryset = shops_models.ShopModel.objects

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(products__product_checks__payment_check__customer=self.owner)
            .distinct()
        )
