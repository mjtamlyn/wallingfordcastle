from django.contrib import admin

from .models import Entry, Series, Tournament


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['rounds']


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'entries_open', 'entries_close']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['rounds']


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'user', 'paid', 'club', 'gender', 'bowstyle', 'agb_number',
        'round', 'notes', 'waiting_list',
    ]
    list_filter = ['tournament', 'paid', 'gender', 'bowstyle', 'round']
