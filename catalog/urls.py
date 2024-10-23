from django.urls import path
from .views import (
    HomeView,
    ContactsView,
    ProductsListView,
    ProductDetailView,
    ProductDeleteView,
    ProductUpdateView,
    ProductCreateView,
    ProductManagementView,
)

app_name = "catalog"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path(
        "products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"
    ),
    path(
        "products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"
    ),
    path(
        "products/<int:product_id>/manage/",
        ProductManagementView.as_view(),
        name="product_management",
    ),
]
