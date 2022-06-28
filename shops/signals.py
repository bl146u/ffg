from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete

from . import models


@receiver(pre_save, sender=models.PaymentCheckModel)
def handler_payment_check_pre_save(
    sender, instance: models.PaymentCheckModel, **kwargs
):
    instance.cost = sum(
        list(map(lambda item: item.cost, instance.product_checks.all()))
    )


@receiver(pre_save, sender=models.ProductCheckModel)
def handler_product_check_pre_save(
    sender, instance: models.ProductCheckModel, **kwargs
):
    instance.cost = instance.price * instance.quantity


@receiver(post_save, sender=models.ProductCheckModel)
def handler_product_check_post_save(
    sender, instance: models.ProductCheckModel, **kwargs
):
    instance.payment_check.save()


@receiver(post_delete, sender=models.ProductCheckModel)
def handler_product_check_post_delete(
    sender, instance: models.ProductCheckModel, **kwargs
):
    instance.payment_check.save()
