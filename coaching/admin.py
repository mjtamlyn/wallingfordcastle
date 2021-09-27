from django.contrib import admin

from .models import TrainingGroup, TrainingGroupType


@admin.register(TrainingGroup)
class TrainingGroupAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'season', 'time', 'number_of_archers']
    list_filter = ['season']
    autocomplete_fields = ['coaches', 'participants']

    def number_of_archers(self, instance):
        return instance.participants.count()


@admin.register(TrainingGroupType)
class TrainingGroupTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'age_group']
