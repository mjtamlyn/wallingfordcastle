from django.contrib import admin, messages

from django_object_actions import (
    DjangoObjectActions, takes_instance_or_queryset,
)

from .models import Achievement


@admin.register(Achievement)
class AchievementAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_filter = ['badge', 'badge_group']
    list_display = ['archer', 'badge', 'badge_group', 'date_awarded', 'paid']
    list_editable = ['paid']
    ordering = ['-date_awarded']
    autocomplete_fields = ['archer']
    actions = change_actions = ['add_invoice_item']

    @takes_instance_or_queryset
    def add_invoice_item(self, request, queryset):
        errors = []
        for achievement in queryset:
            archer = achievement.archer
            if not archer.user.customer_id or not archer.user.subscription_id:
                errors.append(archer.name)
        if errors:
            for archer in errors:
                messages.error(request, '%s does not have an active subscription' % archer)
            return

        for achievement in queryset:
            achievement.archer.user.add_invoice_item(300, '%s %s badge on %s' % (
                achievement.archer,
                achievement.get_badge_display(),
                achievement.date_awarded.strftime('%d/%m/%Y'),
            ))

    add_invoice_item.short_description = 'Add invoice item'
    add_invoice_item.label = 'Add invoice item'
