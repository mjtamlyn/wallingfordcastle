from django.contrib import admin

from .models import TrainingGroup, TrainingGroupType, Trial


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


@admin.register(Trial)
class TrialAdmin(admin.ModelAdmin):
    list_display = ['archer', 'group', 'session_1', 'paid']
