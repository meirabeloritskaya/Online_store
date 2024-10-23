from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from .forms import ProductForm
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View


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


class ProductManagementView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['product.can_unpublish_product',
                           'product.delete_product']

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        if 'unpublish' in request.POST:
            if not request.user.has_perm('product.can_unpublish_product'):
                return HttpResponseForbidden('У вас нет права отменять публикацию')
            product.is_published = False
            product.save()
            return redirect('product_list')

        elif 'delete' in request.POST:
            if not request.user.has_perm('product.delete_product'):
                return HttpResponseForbidden('У вас нет права удалять продукт')
            product.delete()
            return redirect('product_list')

        return HttpResponseForbidden('Некорректное действие')