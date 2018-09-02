import json

from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, UpdateView, View
from django.urls import reverse, reverse_lazy

from braces.views import MessageMixin
import requests
import stripe

from courses.models import Attendee
from membership.models import Member
from wallingford_castle.mixins import FullMemberRequired
from .forms import MemberForm


class Overview(FullMemberRequired, TemplateView):
    template_name = 'membership/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = Member.objects.managed_by(self.request.user).select_related('archer')
        context['monthly_fee'] = sum(member.plan_cost for member in context['members'])
        context['beginners'] = self.request.user.beginner_set.all()
        context['beginners_to_pay'] = sum(beginner.fee for beginner in self.request.user.beginner_set.filter(paid=False))
        context['course_attendees'] = Attendee.objects.filter(archer__user=self.request.user).order_by('course').select_related('archer', 'course')
        context['course_fees_to_pay'] = sum(attendee.fee for attendee in context['course_attendees'] if not attendee.paid)
        context['courses_to_pay_description'] = '; '.join('%s - %s' % (attendee.archer, attendee.course) for attendee in context['course_attendees'] if not attendee.paid)
        context['STRIPE_KEY'] = settings.STRIPE_KEY
        return context


class MemberUpdate(FullMemberRequired, MessageMixin, UpdateView):
    template_name = 'membership/member-update.html'
    form_class = MemberForm
    pk_url_kwarg = 'member_id'
    success_url = reverse_lazy('membership:overview')

    def get_queryset(self):
        return Member.objects.managed_by(self.request.user).select_related('archer')

    def get_object(self):
        obj = super().get_object()
        self.original_plan = obj.plan
        return obj

    def form_valid(self, form):
        response = super().form_valid(form)
        self.messages.success('Details successfully updated!')
        if settings.SLACK_MEMBERSHIP_HREF:
            data = json.dumps({
                'icon_emoji': ':exclamation:',
                'text': '%s has updated details!\n%s' % (
                    self.object.archer.name,
                    self.request.build_absolute_uri(
                        reverse(
                            'admin:membership_member_change',
                            args=(self.object.pk,),
                        )
                    ),
                )
            })
            try:
                requests.post(settings.SLACK_MEMBERSHIP_HREF, data=data)
            except Exception:
                pass
        return response


class PaymentDetails(MessageMixin, View):
    def post(self, request, *args, **kwargs):
        token = request.POST['stripeToken']
        if self.request.user.customer_id:
            customer = stripe.Customer.retrieve(self.request.user.customer_id)
            source = customer.sources.create(source=token)
            customer.default_source = source.id
            customer.save()
        else:
            customer = stripe.Customer.create(
                source=token,
                email=self.request.user.email,
            )
            self.request.user.customer_id = customer.id
            self.request.user.save()
            self.request.user.send_welcome_email()
        self.request.user.update_subscriptions()
        self.messages.success('Thanks! You will receive a confirmation email soon.')
        return HttpResponseRedirect(reverse('membership:overview'))
