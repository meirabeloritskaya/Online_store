from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    return render(request, "home.html")


def contacts(request):
    return render(request, "contacts.html")

def products_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'catalog/products_list.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context)