from django.contrib import admin

from .models import MembershipInterest, BeginnersCourseInterest


class ActionsOnChangeView(object):
    def change_view(self, request, object_id, form_url='', extra_context=None):
        form = self.get_action_form()
        form.fields['action'].choices = self.get_action_choices(request)
        form.fields['select_across'].initial = object_id
        context = {'action_form': form}
        super().change_view(request, object_id, form_url='', extra_context=context)


@admin.register(MembershipInterest)
class MembershipInterestAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'membership_type', 'status']
    list_filter = ['status', 'membership_type', 'age']
    actions = ['make_member']
    readonly_fields = ['created', 'modified']

    def make_member(self, request, queryset):
        for interest in queryset:
            interest.make_member(request)
    make_member.short_description = 'Promote to pending member'
    # TODO: make_member button on admin edit


@admin.register(BeginnersCourseInterest)
class BeginnersCourseInterestAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'modified']
