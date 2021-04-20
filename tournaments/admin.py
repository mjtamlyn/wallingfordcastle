from django.contrib import admin

from .models import Entry, Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'entries_open', 'entries_close']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['rounds']


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['name', 'paid', 'club', 'gender', 'bowstyle', 'agb_number', 'notes']
    list_filter = ['tournament', 'paid', 'gender', 'bowstyle', 'club']
