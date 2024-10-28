from django.views.generic import (
    ListView,
    TemplateView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import get_products_by_category


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

    def get_queryset(self):

        cache_key = "product_list"
        cache_timeout = 60 * 15

        products = cache.get(cache_key)
        if products is None:
            products = Product.objects.all()
            cache.set(cache_key, products, cache_timeout)

        return products


@method_decorator(cache_page(60 * 15), name="dispatch")
class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        if self.request.user.has_perm("catalog.can_unpublish_product"):
            return Product.objects.all()
        else:
            return Product.objects.filter(is_published=True)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_create.html"
    success_url = reverse_lazy("catalog:products_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.is_published = True
        cache.delete("product_list")
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
        cache.delete("product_list")
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
        cache.delete("product_list")
        return super().post(request, *args, **kwargs)

    def user_has_permission(self, product):

        return (
            self.request.user == product.owner
            or self.request.user.has_perm("catalog.can_delete_product")
            or self.request.user.groups.filter(name="Модератор продуктов").exists()
        )


class CategoryListView(ListView):
    model = Category
    template_name = "catalog/category_list.html"  # Шаблон для списка категорий
    context_object_name = "categories"  # Название контекста для шаблона


class CategoryProductsView(ListView):
    model = Product
    template_name = "catalog/category_products.html"
    context_object_name = "products"

    def get_queryset(self):
        """Получает продукты для определённой категории, используя сервисную функцию."""
        category_id = self.kwargs["category_id"]
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs["category_id"]
        context["category"] = Category.objects.get(id=category_id)
        return context
