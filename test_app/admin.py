from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Product
from tomselect_filter.filters import TomSelectListFilter


class CategoryFilter(TomSelectListFilter):
    def get_title(self):
        return _("My Title")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = [("category", CategoryFilter)]


class CustomUserAdmin(DefaultUserAdmin):
    pass

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)