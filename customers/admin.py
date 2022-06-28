from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


UserModel = get_user_model()


@admin.register(UserModel)
class UserAdmin(DjangoUserAdmin):
    pass
