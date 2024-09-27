from django.views.generic import ListView
from .models import Product
from django.views.generic import TemplateView
from django.views.generic import DetailView

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
    slug_field = 'id'  # Используйте, если ваш URL использует slug, иначе можете оставить