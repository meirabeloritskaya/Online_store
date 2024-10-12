from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from django.views.generic import TemplateView
from django.views.generic import DetailView
from .forms import ProductForm
from django.urls import reverse_lazy


class HomeView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = 'products'


class ContactsView(TemplateView):
    template_name = "contacts.html"


class ProductsListView(ListView):
    model = Product
    template_name = 'catalog/products_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    slug_field = 'id'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_create.html'
    success_url = reverse_lazy('products_list')  # Замените на ваш URL для списка продуктов

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_editor.html'
    success_url = reverse_lazy('products_list')  # Замените на ваш URL для списка продуктов

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('products_list')