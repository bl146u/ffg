from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


UserModel = get_user_model()


class ShopModel(models.Model):
    name = models.CharField(verbose_name="Название", max_length=32, unique=True)

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"
        ordering = ("name",)

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    shop = models.ForeignKey(
        ShopModel,
        verbose_name="Магазин",
        on_delete=models.PROTECT,
        related_name="products",
    )
    name = models.CharField(verbose_name="Название", max_length=64)
    price = models.DecimalField(
        verbose_name="Стоимость", max_digits=10, decimal_places=2
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} / {self.shop}"


class PaymentCheckModel(models.Model):
    customer = models.ForeignKey(
        UserModel,
        verbose_name="Покупатель",
        on_delete=models.CASCADE,
        related_name="payment_checks",
    )
    number = models.IntegerField(
        verbose_name="Номер чека", validators=[MinValueValidator(1)]
    )
    date = models.DateTimeField(verbose_name="Дата выдачи", default=timezone.now)
    shop = models.ForeignKey(
        ShopModel,
        verbose_name="Магазин",
        on_delete=models.CASCADE,
        related_name="payment_checks",
    )
    cost = models.DecimalField(
        verbose_name="Общая стоимость", max_digits=10, decimal_places=2
    )

    class Meta:
        verbose_name = "Чек"
        verbose_name_plural = "Чеки"
        ordering = ("-date",)

    def __str__(self):
        return f"# {self.number}: {self.shop} / {self.customer}"

    def clean(self):
        shop = getattr(self, "shop", None)
        if shop:
            shop_list = self.product_checks.values_list("product__shop__pk", flat=True)
            if list(set(map(lambda item: item, shop_list)) - {shop.pk}):
                raise ValidationError(
                    {
                        "shop": f'Чек имеет товары магазина "{ShopModel.objects.get(pk=shop_list[0])}"'
                    }
                )


class ProductCheckModel(models.Model):
    payment_check = models.ForeignKey(
        PaymentCheckModel,
        verbose_name="Чек",
        on_delete=models.CASCADE,
        related_name="product_checks",
    )
    product = models.ForeignKey(
        ProductModel,
        verbose_name="Товар",
        on_delete=models.CASCADE,
        related_name="product_checks",
    )
    quantity = models.IntegerField(
        verbose_name="Количество", validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(
        verbose_name="Стоимость", max_digits=10, decimal_places=2
    )
    cost = models.DecimalField(
        verbose_name="Общая стоимость", max_digits=10, decimal_places=2
    )

    class Meta:
        verbose_name = "Позиция чека"
        verbose_name_plural = "Позиции чеков"

    def __str__(self):
        return f"{self.payment_check} - {self.product}"

    def clean(self):
        payment_check = getattr(self, "payment_check", None)
        product = getattr(self, "product", None)
        if payment_check and product and payment_check.shop != product.shop:
            raise ValidationError("Магазины товара и чека не совпадают")
