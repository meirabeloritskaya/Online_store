from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contacts
from catalog import views

app_name = CatalogConfig.name
urlpatterns = [
    path("", home, name="home"),
    path("contacts/", contacts, name="contacts"),
    path('products/', views.products_list, name='products_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
]
