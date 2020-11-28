import functools

from django import forms
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.views.generic import FormView

from custom_user.admin import EmailUserAdmin
from django_object_actions import (
    DjangoObjectActions, takes_instance_or_queryset,
)

from .models import Archer, MembershipInterest, User


class AddInvoiceItemForm(forms.Form):
    amount = forms.DecimalField(max_digits=5, decimal_places=2)
    description = forms.CharField()


class AddInvoiceItem(FormView):
    template_name = 'admin/wallingford_castle/archer/invoice_item.html'
    form_class = AddInvoiceItemForm

    def get_archers(self):
        selected = self.request.GET['ids'].split(',')
        return Archer.objects.filter(id__in=selected)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opts'] = Archer._meta
        context['title'] = 'Add invoice item'
        context['archers'] = self.get_archers()
        return context

    def form_valid(self, form):
        archers = self.get_archers()
        amount = form.cleaned_data['amount']
        description = form.cleaned_data['description']
        for archer in archers:
            archer.user.add_invoice_item(int(amount * 100), description)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('admin:wallingford_castle_archer_changelist')


@admin.register(Archer)
class ArcherAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['name', 'agb_number', 'date_of_birth', 'age_group']
    search_fields = ['name']
    autocomplete_fields = ['user', 'managing_users']
    actions = change_actions = ['add_invoice_item']

    def get_search_results(self, request, queryset, search_term):
        terms = search_term.split('|')
        result = queryset.none()
        for term in terms:
            next_result, use_distinct = super().get_search_results(request, queryset, term)
            result = result | next_result
        return result, use_distinct

    def get_urls(self):
        urls = super().get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return functools.update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urls.insert(
            0,
            path('invoice/', wrap(AddInvoiceItem.as_view()), name='%s_%s_invoice_item' % info),
        )
        return urls

    @takes_instance_or_queryset
    def add_invoice_item(self, request, queryset):
        errors = []
        for archer in queryset:
            if not archer.user.customer_id or not archer.user.subscription_id:
                errors.append(archer.name)
        if errors:
            for archer in errors:
                messages.error(request, '%s does not have an active subscription' % archer)
            return

        url = reverse('admin:%s_%s_invoice_item' % (self.model._meta.app_label, self.model._meta.model_name))
        return HttpResponseRedirect(url + '?ids=%s' % ','.join(str(item.pk) for item in queryset))
    add_invoice_item.short_description = 'Add invoice item'
    add_invoice_item.label = 'Add invoice item'


class ArcherDataMixin(object):
    """Utility mixin class for ModelAdmins which reference archer data."""

    def archer_name(self, obj):
        return obj.archer.name
    archer_name.short_description = 'Name'

    def archer_age(self, obj):
        return obj.archer.get_age_display()
    archer_age.short_description = 'Age'

    def archer_agb_number(self, obj):
        return obj.archer.agb_number
    archer_agb_number.short_description = 'AGB number'

    def archer_date_of_birth(self, obj):
        return obj.archer.date_of_birth
    archer_date_of_birth.short_description = 'DOB'

    def archer_age_group(self, obj):
        return obj.archer.age_group
    archer_age_group.short_description = 'Age group'
    archer_age_group.admin_order_field = 'archer__date_of_birth'

    def archer_address(self, obj):
        return obj.archer.address
    archer_address.short_description = 'Address'

    def archer_contact_number(self, obj):
        return obj.archer.contact_number
    archer_contact_number.short_description = 'Contact number'

    def archer_email(self, obj):
        return obj.archer.user.email
    archer_email.short_description = 'Contact email'


@admin.register(MembershipInterest)
class MembershipInterestAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['name', 'age', 'membership_type', 'status']
    list_filter = ['status', 'membership_type', 'age']
    actions = change_actions = ['make_member', 'send_to_beginners']
    readonly_fields = ['created', 'modified']

    @takes_instance_or_queryset
    def make_member(self, request, queryset):
        users = set()
        for interest in queryset:
            member = interest.make_member(request)
            if member:
                users.add(member.archer.user)
        for user in users:
            if user.customer_id:
                user.update_subscriptions()
                user.send_welcome_email()
    make_member.short_description = 'Promote to pending member'
    make_member.label = 'Make pending member'

    @takes_instance_or_queryset
    def send_to_beginners(self, request, queryset):
        for interest in queryset:
            interest.send_to_beginners()
    send_to_beginners.short_description = 'Send to beginners course'
    send_to_beginners.label = 'Send to beginners course'


@admin.register(User)
class UserAdmin(DjangoObjectActions, EmailUserAdmin):
    actions = change_actions = ['send_new_user_email', 'send_welcome_email']
    fieldsets = EmailUserAdmin.fieldsets + (
        ('Internal fields', {
            'fields': ('customer_id', 'subscription_id', 'tournament_only', 'generate_register_url')
        }),
    )
    readonly_fields = ['generate_register_url']

    def generate_register_url(self, instance):
        return instance.generate_register_url()

    @takes_instance_or_queryset
    def send_new_user_email(self, request, queryset):
        for user in queryset:
            user.send_new_user_email(request)
    send_new_user_email.short_description = 'Send new user email'
    send_new_user_email.label = 'Send new user email'

    @takes_instance_or_queryset
    def send_welcome_email(self, request, queryset):
        for user in queryset:
            user.send_welcome_email(request)
    send_welcome_email.short_description = 'Send welcome email'
    send_welcome_email.label = 'Send welcome email'
