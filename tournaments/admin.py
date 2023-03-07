from django.contrib import admin, messages
from django.utils.html import mark_safe

from .models import Entry, Series, Tournament


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['rounds']


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'entries', 'entries_open', 'entries_close']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['rounds']

    def entries(self, instance):
        total = instance.entry_set.count()
        summary = instance.entry_summary()
        if summary:
            return mark_safe('%s Entries<br />%s' % (total, summary))
        return '%s Entries' % total


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'user', 'paid', 'club', 'gender', 'bowstyle', 'agb_number',
        'round', 'date_of_birth', 'notes', 'waiting_list',
    ]
    list_filter = ['tournament', 'paid', 'gender', 'bowstyle', 'round', 'series_entry']
    actions = ['add_invoice_item']

    def add_invoice_item(self, request, queryset):
        errors = []
        for entry in queryset:
            user = entry.user
            if not user.customer_id or not user.subscription_id:
                errors.append(entry.name)
        if errors:
            for archer in errors:
                messages.error(request, '%s does not have an active subscription' % archer)
            return

        for entry in queryset:
            entry.user.add_invoice_item(entry.tournament.entry_fee * 100, '%s entry to %s' % (
                entry,
                entry.tournament,
            ))
            entry.paid = True
            entry.save()
