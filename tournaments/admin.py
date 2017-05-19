from django.contrib import admin

from .models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['name', 'paid', 'club', 'gender', 'bowstyle']
    list_filter = ['paid', 'club', 'gender', 'bowstyle']
