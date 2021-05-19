from django import forms
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import Category, Product


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name', )

    def clean(self):
        cleaned_data = super().clean()
        if slugify(cleaned_data['category_name']) in [cat.slug for cat in Category.objects.all()]:
            raise ValidationError("Podana kategoria już istnieje !")


class EditCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name', )

    def clean(self):
        cleaned_data = super().clean()
        if slugify(cleaned_data['category_name']) in [cat.slug for cat in Category.objects.all()]:
            raise ValidationError("Podana kategoria już istnieje !")


class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'vat', 'stock', 'categories', )


class SearchProductForm(forms.Form):
    search = forms.CharField(max_length=64, label='Wyszukaj produkt lub kategorie')
