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

    def get_model(self):
        return Inventory


class ItemProductFilter(TomSelectListFilter):
    def get_title(self):
        return _("By Products")

    def get_model(self):
        return Product


class InventoryProductFilter(TomSelectListFilter):
    def get_title(self):
        return _("By Products")

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
        ("inventories__id", InventoryFilter),
    ]
    search_fields = ["name"]

    def lookup_allowed(self, lookup, value, request=None):
        if lookup.startswith("inventory__products__id"):
            return True
        return super().lookup_allowed(lookup, value)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    search_fields = ["name"]

    list_filter = [
        ("product__pk", ItemProductFilter),
    ]


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    filter_horizontal = [
        "products",
    ]

    list_filter = [
        ("products__id", InventoryProductFilter),
    ]


class CustomUserAdmin(DefaultUserAdmin):
    pass


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
