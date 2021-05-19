from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, FormView
from django.views.generic.base import View

from .forms import AddCategoryForm, EditCategoryForm, EditProductForm, SearchProductForm
from .models import Category, Product


class CategoriesView(View):
    def get(self, request):
        categories = Category.objects.all().order_by('category_name')
        context = {
            'categories': categories
        }
        return render(request, 'homework_app/categories.html', context)


class CategoryView(View):
    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(categories=category)
        brutto = [(product, round(float(product.price) * (1 + product.vat), 2)) for product in products]
        context = {
            'brutto': brutto
        }
        return render(request, 'homework_app/category.html', context)


class ProductView(View):

    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        return render(request, "homework_app/product_details.html", {"product": product})


class AddCategoryView(PermissionRequiredMixin, CreateView):
    model = Category
    form_class = AddCategoryForm
    success_url = reverse_lazy('categories')
    permission_required = 'homework_app.add_category'


class EditCategoryView(PermissionRequiredMixin, UpdateView):
    model = Category
    form_class = EditCategoryForm
    success_url = reverse_lazy('categories')
    permission_required = 'homework_app.change_category'


class ProductsView(ListView):
    model = Product
    ordering = 'name'


class EditProductView(PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = EditProductForm
    success_url = reverse_lazy('products')
    permission_required = 'homework_app.change_product'


class AddProductView(PermissionRequiredMixin, CreateView):
    model = Product
    form_class = EditProductForm
    success_url = reverse_lazy('products')
    permission_required = 'homework_app.add_product'


class SearchProductView(FormView):
    model = Product
    form_class = SearchProductForm
    success_url = reverse_lazy('search_product')
    template_name = 'homework_app/search.html'

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        name = form.cleaned_data['search']
        products = Product.objects.filter(Q(name__icontains=name) | Q(categories_name__icontains=name))

        return render(self.request, self.template_name, context={'products': products, 'form': form})
