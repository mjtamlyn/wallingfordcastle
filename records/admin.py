from django.contrib import admin

from .models import Achievement


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_filter = ['badge', 'badge_group']
    list_display = ['archer', 'badge', 'badge_group', 'date_awarded', 'paid']
    list_editable = ['paid']
    ordering = ['-date_awarded']
    autocomplete_fields = ['archer']
