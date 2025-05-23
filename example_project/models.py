from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

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

    def __str__(self):
        return self.name


class Inventory(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(
        to=Product,
        related_name="inventory",
    )

    def __str__(self):
        return self.name
