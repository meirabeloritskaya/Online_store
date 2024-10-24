from django.views.generic import (
    ListView,
    TemplateView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Product
from .forms import ProductForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products"


class ContactsView(TemplateView):
    template_name = "contacts.html"


class ProductsListView(ListView):
    model = Product
    template_name = "catalog/products_list.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"
    slug_field = "id"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_create.html"
    success_url = reverse_lazy("catalog:products_list")


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_editor.html"
    success_url = reverse_lazy("catalog:products_list")

    def form_valid(self, form):
        if not self.request.user.has_perm("catalog.can_edit_product"):
            # Добавляем флеш-сообщение
            messages.error(self.request, "У вас нет прав на редактирование продукта.")
            # Перенаправляем на предыдущую страницу или список продуктов
            return HttpResponseRedirect(
                self.request.META.get("HTTP_REFERER", self.success_url)
            )
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:products_list")

    def post(self, request, *args, **kwargs):

        if not request.user.has_perm("catalog.can_delete_product"):

            messages.error(request, "У вас нет прав на удаление продукта.")

            return HttpResponseRedirect(
                request.META.get("HTTP_REFERER", self.success_url)
            )
        return super().post(request, *args, **kwargs)
