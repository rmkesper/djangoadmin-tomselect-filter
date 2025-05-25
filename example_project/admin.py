from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

from tomselect_filter.filters import TomSelectListFilter

from .models import AccountingYear, Inventory, Item, Product


class AccountingYearFilter(TomSelectListFilter):
    def get_title(self):
        return _("By Accounting Year")

    def get_model(self):
        return AccountingYear

    def get_admin_model(self):
        return AccountingYear


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

    def get_admin_model(self):
        return Item

    def get_custom_queryset(self, term=None):
        """Demo use of a fully custom queryset."""
        qs = Product.objects.filter(id=1)
        return JsonResponse(
            [{"value": obj.id, "label": obj.name} for obj in qs], safe=False
        )


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
        "accounting_year",
    ]
    autocomplete_fields = [
        "accounting_year",
    ]
    list_filter = [
        ("accounting_year__id", AccountingYearFilter),
        ("category", CategoryFilter),
        ("items__name", ItemFilter),
        ("inventories__id", InventoryFilter),
    ]
    search_fields = ["name"]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "accounting_year",
    ]
    search_fields = ["name"]
    autocomplete_fields = [
        "accounting_year",
        "product",
    ]
    list_filter = [
        ("product__id", ItemProductFilter),
    ]


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "accounting_year",
    ]
    search_fields = ["name"]
    filter_horizontal = [
        "products",
    ]
    autocomplete_fields = [
        "accounting_year",
    ]
    list_filter = [
        ("products__id", InventoryProductFilter),
    ]


@admin.register(AccountingYear)
class AccountingYearAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
    search_fields = [
        "name",
    ]


class CustomUserAdmin(DefaultUserAdmin):
    pass


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
