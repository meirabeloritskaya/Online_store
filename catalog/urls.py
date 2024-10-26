from django.urls import path
from .views import (
    HomeView,
    ContactsView,
    CategoryProductsView,
    ProductsListView,
    ProductDetailView,
    ProductDeleteView,
    ProductUpdateView,
    ProductCreateView,
)
from django.views.decorators.cache import cache_page

app_name = "catalog"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path(
        "products/<int:pk>/",
        cache_page(60)(ProductDetailView.as_view(), name="product_detail"),
    ),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path(
        "products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"
    ),
    path(
        "products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"
    ),
    path(
        "category/<int:category_id>/",
        CategoryProductsView.as_view(),
        name="category_products",
    ),
]
