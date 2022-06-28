from django.contrib import admin

from . import models


class ProductCheckInline(admin.TabularInline):
    model = models.ProductCheckModel
    show_change_link = True

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False
