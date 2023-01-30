import json

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, TemplateView, UpdateView, View

import requests
import stripe
from braces.views import MessageMixin

from beginners.models import STATUS_FAST_TRACK, STATUS_ON_COURSE
from coaching.forms import TrialContinueForm
from coaching.models import Trial
from courses.models import Attendee, Course
from membership.models import Member
from records.models import Achievement
from wallingford_castle.mixins import FullMemberRequired

from .forms import MemberForm


class Overview(FullMemberRequired, TemplateView):
    template_name = 'membership/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = Member.objects.managed_by(self.request.user).select_related('archer')
        context['monthly_fee'] = sum(
            member.plan_cost for member in context['members'] if member.archer.user == self.request.user
        )
        context['beginners'] = self.request.user.beginner_set.all()
        context['beginners_to_pay'] = sum(
            beginner.fee for beginner in self.request.user.beginner_set.filter(
                paid=False,
                status__in=[STATUS_ON_COURSE, STATUS_FAST_TRACK],
            )
        )
        context['trials'] = Trial.objects.filter_ongoing().filter(
            archer__user=self.request.user,
        ).select_related('archer', 'group')
        context['trials_to_pay'] = sum(
            trial.fee for trial in context['trials'] if not trial.paid
        )
        context['completed_trials'] = Trial.objects.filter_completed().filter(
            archer__user=self.request.user,
        ).select_related('archer', 'group')
        for trial in context['completed_trials']:
            trial.form = TrialContinueForm(trial=trial)
        context['course_attendees'] = Attendee.objects.filter(
            archer__user=self.request.user,
            course__can_book_individual_sessions=False,
            member=False,
        ).order_by('course').select_related('archer', 'course')
        context['course_fees_to_pay'] = sum(
            attendee.fee for attendee in context['course_attendees'] if not attendee.paid
        )
        if not context['members']:
            context['bookable_courses'] = Course.objects.filter(
                open_for_bookings=True,
                open_to_non_members=True,
            )
        context['STRIPE_KEY'] = settings.STRIPE_KEY

        achievements = Achievement.objects.filter(
            archer__in=[member.archer for member in context['members']],
        ).order_by('-date_awarded')
        for achievement in achievements:
            for member in context['members']:
                if member.archer_id == achievement.archer_id:
                    if not hasattr(member, 'achievements'):
                        member.achievements = []
                    member.achievements.append(achievement)
        return context


class MemberAttendance(FullMemberRequired, DetailView):
    model = Member
    template_name = 'membership/attendance.html'
    pk_url_kwarg = 'member_id'

    def get_queryset(self):
        return Member.objects.managed_by(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['archer'] = self.object.archer
        context['attendance_record'] = self.object.archer.event_attendance_set.order_by(
            '-event__date'
        ).select_related('event')
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
    def get(self, request, *args, **kwargs):
        membership_overview_url = reverse('membership:overview')
        customer_id = self.request.user.customer_id or None
        subscription_id = self.request.user.subscription_id or None
        if not subscription_id or not customer_id:
            # TODO
            self.messages.error('You currently do not have a subscription set up, please contact Marc for help.')
            return redirect(membership_overview_url)
        else:
            session = stripe.checkout.Session.create(
                mode='setup',
                customer=customer_id,
                payment_method_types=['card'],
                success_url=self.request.build_absolute_uri(membership_overview_url),
                cancel_url=self.request.build_absolute_uri(membership_overview_url),
            )
            return redirect(session.url, status_code=303)


class RangeBooking(FullMemberRequired, TemplateView):
    template_name = 'membership/range_booking.html'
