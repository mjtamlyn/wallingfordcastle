from django.contrib import admin

from .models import Category, Round


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'category']
    list_filter = ['category']
