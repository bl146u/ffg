from admin_auto_filters.filters import AutocompleteFilter


class ProductShopFilter(AutocompleteFilter):
    title = "Магазин"
    field_name = "shop"


class PaymentCheckCustomerFilter(AutocompleteFilter):
    title = "Покупатель"
    field_name = "customer"


class PaymentCheckShopFilter(AutocompleteFilter):
    title = "Магазин"
    field_name = "shop"


class ProductCheckPaymentCheckFilter(AutocompleteFilter):
    title = "Чек"
    field_name = "payment_check"


class ProductCheckProductFilter(AutocompleteFilter):
    title = "Товар"
    field_name = "product"
