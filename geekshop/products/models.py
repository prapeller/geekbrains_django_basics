from django.db import models
from django.urls import reverse
from djmoney.models.fields import MoneyField


# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('admins_app:category_list')


class Product(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='product_images', blank=True)
    description = models.TextField(blank=True)
    # price = MoneyField(max_digits=8, decimal_places=2, default_currency='₽')
    price = models.DecimalField(max_digits=8,decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return self.name
