from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from .forms import ProductForm
from django.urls import reverse_lazy
from .mixins import LoginRequiredMixin



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


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_create.html'
    success_url = reverse_lazy('products_list')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_editor.html'
    success_url = reverse_lazy('products_list')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('products_list')