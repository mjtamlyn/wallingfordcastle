from django.contrib import admin

from .models import Entry, Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'entries_open', 'entries_close']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['name', 'paid', 'club', 'gender', 'bowstyle']
    list_filter = ['tournament', 'paid', 'club', 'gender', 'bowstyle']
