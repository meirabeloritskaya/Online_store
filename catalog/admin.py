from django.contrib import admin

from .models import Category, Product

@admin.register(Category)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name', 'description',)

@admin.register(Product)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)