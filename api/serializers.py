from rest_framework import serializers

from django.contrib.auth import get_user_model

from shops import models as shops_models


UserModel = get_user_model()


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("pk", "first_name", "last_name", "email", "username")


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = shops_models.ShopModel
        fields = ("pk", "name")


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()

    class Meta:
        model = shops_models.ProductModel
        fields = ("pk", "name", "price")


class ProductShopSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()
    shop = ShopSerializer()

    class Meta:
        model = shops_models.ProductModel
        fields = ("pk", "name", "price", "shop")


class ProductChecksSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()
    cost = serializers.FloatField()
    details = ProductSerializer(source="product")

    class Meta:
        model = shops_models.ProductCheckModel
        fields = ("pk", "quantity", "price", "cost", "details")


class ProductChecksShopSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()
    cost = serializers.FloatField()
    details = ProductShopSerializer(source="product")

    class Meta:
        model = shops_models.ProductCheckModel
        fields = ("pk", "quantity", "price", "cost", "details")


class CheckSerializer(serializers.ModelSerializer):
    shop = ShopSerializer()
    cost = serializers.FloatField()
    products = serializers.ListSerializer(
        child=ProductChecksSerializer(), source="product_checks"
    )

    class Meta:
        model = shops_models.PaymentCheckModel
        fields = ("pk", "number", "date", "cost", "shop", "products")


class CheckCustomerSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    shop = ShopSerializer()
    cost = serializers.FloatField()
    products = serializers.ListSerializer(
        child=ProductChecksSerializer(), source="product_checks"
    )

    class Meta:
        model = shops_models.PaymentCheckModel
        fields = ("pk", "number", "date", "cost", "customer", "shop", "products")


class ImportProductChecksSerializer(serializers.ModelSerializer):
    details = serializers.PrimaryKeyRelatedField(
        queryset=shops_models.ProductModel.objects, source="product"
    )

    class Meta:
        model = shops_models.ProductCheckModel
        fields = ("pk", "quantity", "price", "cost", "details")


class ImportCheckSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects)
    shop = serializers.PrimaryKeyRelatedField(queryset=shops_models.ShopModel.objects)
    products = ImportProductChecksSerializer(many=True, source="product_checks")

    class Meta:
        model = shops_models.PaymentCheckModel
        fields = ("pk", "number", "date", "cost", "customer", "shop", "products")

    def create(self, validated_data):
        products = validated_data.pop("product_checks")
        check = super().create(validated_data)
        for product in products:
            instance = shops_models.ProductCheckModel(
                **{**dict(product), "payment_check": check}
            )
            instance.save()
        return check


class ImportChecksSerializer(serializers.ListSerializer):
    child = ImportCheckSerializer()
