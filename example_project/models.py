from django.db import models


def get_default_accounting_year():
    if accounting_year := AccountingYear.objects.filter(is_default=True).first():
        return accounting_year
    return None


def get_default_accounting_year_id():
    return getattr(get_default_accounting_year(), "id", None)


class AccountingYear(models.Model):
    name = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            (
                "name",
                "is_default",
            ),
        )


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    accounting_year = models.ForeignKey(
        to=AccountingYear,
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(
        to=Product,
        related_name="items",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    accounting_year = models.ForeignKey(
        to=AccountingYear,
        related_name="items",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Inventory(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(
        to=Product,
        related_name="inventories",
    )
    accounting_year = models.ForeignKey(
        to=AccountingYear,
        related_name="inventories",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name
