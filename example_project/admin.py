from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from tomselect_filter.filters import TomSelectListFilter

from .models import Inventory, Item, Product


class CategoryFilter(TomSelectListFilter):
    def get_title(self):
        return _("My Title")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = [("category", CategoryFilter)]
    search_fields = ["name"]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    filter_horizontal = [
        "products",
    ]


class CustomUserAdmin(DefaultUserAdmin):
    pass


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
