from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = (
        "name",
        "description",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "category",
        "owner",  # Добавляем владельца
    )
    list_filter = ("category", "owner")  # Добавляем фильтр по владельцу
    search_fields = (
        "name",
        "description",
        "owner__email",  # Позволяет искать по email владельца
    )
