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
from django.shortcuts import redirect


class HomeView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products"

    def get_queryset(self):

        return Product.objects.filter(is_published=True)


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

    def get_queryset(self):

        if self.request.user.has_perm("catalog.can_unpublish_product"):
            return Product.objects.all()
        else:
            return Product.objects.filter(is_published=True)

    def post(self, request, *args, **kwargs):
        product = self.get_object()

        print(f"Before: {product.is_published}")  # Для отладки
        product.is_published = "is_published" in request.POST
        product.save()
        print(f"After: {product.is_published}")  # Для отладки

        messages.success(request, "Статус продукта обновлен.")

        return redirect("catalog:product_detail", pk=product.pk)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_create.html"
    success_url = reverse_lazy("catalog:products_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.is_published = True
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_editor.html"
    success_url = reverse_lazy("catalog:products_list")

    def form_valid(self, form):
        product = self.get_object()

        if not self.user_has_permission(product):
            messages.error(self.request, "У вас нет прав на редактирование продукта.")
            return HttpResponseRedirect(
                self.request.META.get("HTTP_REFERER", self.success_url)
            )

        return super().form_valid(form)

    def user_has_permission(self, product):

        return (
            self.request.user == product.owner
            or self.request.user.has_perm("catalog.can_edit_product")
            or self.request.user.groups.filter(name="Модератор продуктов").exists()
        )


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:products_list")

    def post(self, request, *args, **kwargs):
        product = self.get_object()

        if not self.user_has_permission(product):
            messages.error(request, "У вас нет прав на удаление продукта.")
            return HttpResponseRedirect(
                request.META.get("HTTP_REFERER", self.success_url)
            )

        return super().post(request, *args, **kwargs)

    def user_has_permission(self, product):

        return (
            self.request.user == product.owner
            or self.request.user.has_perm("catalog.can_delete_product")
            or self.request.user.groups.filter(name="Модератор продуктов").exists()
        )
