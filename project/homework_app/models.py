from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from django.utils.text import slugify

VAT = (
    (0, "0%"),
    (0.05, "5%"),
    (0.08, "8%"),
    (0.23, "23%"),
)


class Category(models.Model):
    category_name = models.CharField(max_length=64, verbose_name='Kategoria')
    slug = models.SlugField(max_length=64, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)
        return self.slug

    def __str__(self):
        return self.category_name


class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    vat = models.FloatField(choices=VAT)
    stock = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category)
