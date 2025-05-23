from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from tomselect_filter.filters import TomSelectListFilter

from .models import Inventory, Item, Product


class CategoryFilter(TomSelectListFilter):
    def get_title(self):
        return _("By Categories")


class ItemFilter(TomSelectListFilter):
    def get_title(self):
        return _("By Items")


class InventoryFilter(TomSelectListFilter):
    def get_title(self):
        return _("By Inventory")

    def get_mode(self):
        return "pk__in"


class ItemProductFilter(TomSelectListFilter):
    def get_title(self):
        return _("By Products")

    def get_mode(self):
        return "pk"

    def get_model(self):
        return Product


class InventoryProductFilter(TomSelectListFilter):
    def get_title(self):
        return _("By Products")

    def get_mode(self):
        return "pk"

    def get_model(self):
        return Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
    ]

    list_filter = [
        ("category", CategoryFilter),
        ("items__name", ItemFilter),
        ("inventory", InventoryFilter),
    ]
    search_fields = ["name"]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    search_fields = ["name"]

    list_filter = [
        ("product", ItemProductFilter),
    ]


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    filter_horizontal = [
        "products",
    ]

    list_filter = [
        ("products", InventoryProductFilter),
    ]


class CustomUserAdmin(DefaultUserAdmin):
    pass


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
