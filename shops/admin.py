from daterange.filters import DateRangeFilter

from django.contrib import admin

from . import models, filters, inlines


@admin.register(models.ShopModel)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    search_fields = ("name",)


@admin.register(models.ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("__str__", "shop", "price")
    search_fields = ("name",)
    list_filter = (filters.ProductShopFilter,)
    autocomplete_fields = ("shop",)


@admin.register(models.PaymentCheckModel)
class PaymentCheckAdmin(admin.ModelAdmin):
    list_display = ("__str__", "customer", "number", "shop", "cost", "date")
    search_fields = ("number",)
    list_filter = (
        filters.PaymentCheckCustomerFilter,
        filters.PaymentCheckShopFilter,
        ("date", DateRangeFilter),
    )
    autocomplete_fields = ("customer", "shop")
    readonly_fields = ("cost",)
    inlines = (inlines.ProductCheckInline,)

    class Media:
        css = {"all": ("admin/css/forms.css", "css/admin/daterange.css")}
        js = ("admin/js/calendar.js", "js/admin/DateRangeShortcuts.js")


@admin.register(models.ProductCheckModel)
class ProductCheckAdmin(admin.ModelAdmin):
    list_display = ("__str__", "payment_check", "product", "quantity", "price", "cost")
    list_filter = (
        filters.ProductCheckPaymentCheckFilter,
        filters.ProductCheckProductFilter,
    )
    autocomplete_fields = ("payment_check", "product")
    readonly_fields = ("cost",)
