import datetime
import json

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Prefetch, Q
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView, FormView, ListView, TemplateView, View,
)
from django.views.generic.detail import SingleObjectMixin

import requests
import stripe
from braces.views import MessageMixin
from dateutil.relativedelta import relativedelta

from membership.models import Member
from payments.models import Checkout
from wallingford_castle.forms import DirectRegisterForm
from wallingford_castle.mixins import FullMemberRequired
from wallingford_castle.models import Archer

from .forms import (
    CourseInterestForm, MembersBookCourseForm, NonMembersBookCourseForm,
    SessionBookingForm,
)
from .models import Attendee, Course, Session


class Holidays(TemplateView):
    template_name = 'courses/holidays.html'


class HolidaysUtils:
    def dispatch(self, request, *args, **kwargs):
        try:
            self.course = Course.objects.get(can_book_individual_sessions=True, open_for_bookings=True)
        except Course.DoesNotExist:
            self.messages.error('Bookings are not currently open, sorry. Please contact us for more information.')
            return redirect('courses:holidays')
        return super().dispatch(request, *args, **kwargs)

    def get_members(self):
        return Member.objects.managed_by(self.request.user).filter(archer__age='junior').select_related('archer')

    def get_archers(self, members):
        member_archers = [member.archer for member in members]
        other_archers = Archer.objects.filter(
            Q(user=self.request.user) | Q(managing_users=self.request.user),
            age='junior',
        ).exclude(id__in=[archer.pk for archer in member_archers])
        return other_archers

    def annotate_with_details(self, archer, errored_booking_forms=None):
        if errored_booking_forms is None:
            errored_booking_forms = {}
        try:
            archer.attendee = archer.attendee_set.get(course=self.course)
            archer.sessions_booked = archer.attendee.session_set.order_by('session__start_time')
            archer.booking_form = errored_booking_forms.get(
                str(archer.pk),
                SessionBookingForm(course=self.course, booked=archer.sessions_booked, prefix=archer.pk),
            )
        except Attendee.DoesNotExist:
            archer.attendee = None
            archer.booking_form = SessionBookingForm(course=self.course, prefix=archer.pk)
        return archer

    def get_to_pay(self, archers, members):
        to_pay = 0
        sessions = []
        for archer in archers:
            if archer.attendee:
                for session in archer.sessions_booked:
                    if not session.paid:
                        sessions.append(session)
                        to_pay += session.fee
        for member in members:
            if member.archer.attendee:
                for session in member.archer.sessions_booked:
                    if not session.paid:
                        sessions.append(session)
                        to_pay += session.fee
        return sessions, to_pay


class HolidaysBook(HolidaysUtils, MessageMixin, TemplateView):
    template_name = 'courses/holidays-book.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_anonymous:
            context.setdefault('login_form', AuthenticationForm())
            context.setdefault('register_form', DirectRegisterForm())
        else:
            context['members'] = self.get_members()
            context['archers'] = self.get_archers(context['members'])

            for member in context['members']:
                member.archer = self.annotate_with_details(member.archer, context.get('errored_booking_forms'))
            for archer in context['archers']:
                self.annotate_with_details(archer, context.get('errored_booking_forms'))

            form = CourseInterestForm(initial={'contact_email': self.request.user.email}, course_type='holidays')
            context.setdefault('new_archer_form', form)

            _, context['to_pay'] = self.get_to_pay(context['archers'], context['members'])
            context['STRIPE_KEY'] = settings.STRIPE_KEY

        return context

    def post(self, request, *args, **kwargs):
        context = {}
        form = request.POST.get('form')
        if form == 'login':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                login(request, form.user_cache)
                return self.get(request, *args, **kwargs)
            else:
                context['login_form'] = form
        elif form == 'register':
            form = DirectRegisterForm(data=request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return self.get(request, *args, **kwargs)
            else:
                context['register_form'] = form
        elif form == 'new-archer':
            form = CourseInterestForm(data=request.POST, course_type='holidays')
            if form.is_valid():
                today = datetime.date.today()
                age = relativedelta(today, form.instance.date_of_birth).years
                if age >= 13:
                    msg = (
                        'Holiday archery is only available for under 13s. For '
                        'older children, please book a beginners course.'
                    )
                    form.add_error(None, msg)
                    context['new_archer_form'] = form
                else:
                    interest = form.save()
                    interest.convert_to_archer(self.request.user)
                    return self.get(request, *args, **kwargs)
            else:
                context['new_archer_form'] = form
        elif form == 'booking':
            archer_id = request.POST['archer']
            form = SessionBookingForm(data=request.POST, course=self.course, prefix=archer_id)
            if form.is_valid():
                try:
                    form.save(archer_id=archer_id)
                    return self.get(request, *args, **kwargs)
                except SessionBookingForm.CancellationException:
                    msg = (
                        'To cancel a session which has been paid for, please '
                        'email us at hello@wallingfordcastle.co.uk'
                    )
                    form.add_error(None, msg)
                    context['errored_booking_forms'] = {archer_id: form}
        elif form == 'add-to-subscription':
            if self.request.user.subscription_id:
                members = self.get_members()
                archers = self.get_archers(members)
                for member in members:
                    member.archer = self.annotate_with_details(member.archer)
                for archer in archers:
                    self.annotate_with_details(archer)
                description = 'Holiday archery'
                _, amount = self.get_to_pay(archers, members)
                self.request.user.add_invoice_item(
                    amount=amount * 100,
                    description=description,
                )
                for member in members:
                    for session in getattr(member.archer, 'sessions_booked', []):
                        session.paid = True
                        session.save()
                for archer in archers:
                    for session in getattr(archer, 'sessions_booked', []):
                        session.paid = True
                        session.save()
                self.messages.success(
                    'Thanks for booking your holiday session! We will contact you '
                    'soon with more details.'
                )
            else:
                self.messages.error('You do not seem to have an active membership.')
        return self.render_to_response(context=self.get_context_data(**context))


class HolidaysPay(HolidaysUtils, MessageMixin, View):
    def get(self, request, *args, **kwargs):
        customer_id = self.request.user.customer_id or None
        return_url = reverse('courses:holidays')
        members = self.get_members()
        archers = self.get_archers(members)
        for archer in archers:
            self.annotate_with_details(archer)
        to_pay, _ = self.get_to_pay(archers, members)
        if not to_pay:
            self.messages.error('You have no sessions to pay for.')
            return redirect(return_url)
        stripe_session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'gbp',
                    'product_data': {
                        'name': 'Holiday archery session - %s on %s' % (
                            session.attendee.archer,
                            session.session.start_time.date().strftime('%-d %B %Y'),
                        ),
                    },
                    'unit_amount': session.fee * 100,
                },
                'quantity': 1,
            } for session in to_pay],
            mode='payment',
            customer=customer_id,
            customer_email=None if customer_id else self.request.user.email,
            customer_creation=None if customer_id else 'always',
            success_url=request.build_absolute_uri(return_url),
            cancel_url=request.build_absolute_uri(return_url),
        )
        intent = Checkout.objects.create(stripe_id=stripe_session.id, user=self.request.user)
        for session in to_pay:
            intent.lineitemintent_set.create(item=session)
        return redirect(stripe_session.url, status_code=303)


class SchoolSignup(MessageMixin, FormView):
    form_class = CourseInterestForm
    school = None

    def get_template_names(self):
        return ['courses/%s.html' % self.school]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['course_type'] = self.school
        return kwargs

    def form_valid(self, form):
        form.save()
        self.messages.success('Thanks for your interest! We will be in touch soon.')
        if settings.SLACK_EVENTS_HREF:
            data = json.dumps({
                'icon_emoji': ':wave:',
                'text': 'New %s course interest received for %s!\n%s' % (
                    self.school,
                    form.cleaned_data['name'],
                    self.request.build_absolute_uri(
                        reverse(
                            'admin:courses_interest_change',
                            args=(form.instance.pk,),
                        )
                    ),
                )
            })
            try:
                requests.post(settings.SLACK_EVENTS_HREF, data=data)
            except Exception:
                pass
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('juniors')


class MembersCourseList(FullMemberRequired, ListView):
    model = Course
    template_name = 'courses/members_course_list.html'

    def get_queryset(self):
        bookable_courses = Course.objects.filter(open_for_bookings=True, open_to_members=True).prefetch_related(
            Prefetch('session_set', queryset=Session.objects.order_by('start_time'), to_attr='sessions')
        ).order_by('id')
        for course in bookable_courses:
            user = self.request.user
            course.registered_members = (
                course.attendee_set.filter(archer__user=user) |
                course.attendee_set.filter(archer__managing_users=user)
            )
        return bookable_courses


class MembersCourseBooking(FullMemberRequired, SingleObjectMixin, FormView):
    model = Course
    template_name = 'courses/members_book_course.html'
    context_object_name = 'course'
    form_class = MembersBookCourseForm

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Course.objects.filter(open_for_bookings=True, open_to_members=True)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'course': self.object,
            'user': self.request.user,
        })
        return kwargs

    def form_valid(self, form):
        attendee = form.save()
        if settings.SLACK_EVENTS_HREF:
            data = json.dumps({
                'icon_emoji': ':white_check_mark:',
                'text': '%s has registered for %s!' % (
                    attendee.archer,
                    attendee.course,
                )
            })
            try:
                requests.post(settings.SLACK_EVENTS_HREF, data=data)
            except Exception:
                pass
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('courses:members-course-list')


class NonMembersCourseList(FullMemberRequired, ListView):
    model = Course
    template_name = 'courses/non_members_course_list.html'

    def get_queryset(self):
        bookable_courses = Course.objects.filter(open_for_bookings=True, open_to_non_members=True).prefetch_related(
            Prefetch('session_set', queryset=Session.objects.order_by('start_time'), to_attr='sessions')
        )
        for course in bookable_courses:
            user = self.request.user
            course.registered_archers = (
                course.attendee_set.filter(archer__user=user) |
                course.attendee_set.filter(archer__managing_users=user)
            )
        return bookable_courses


class NonMembersCourseBooking(FullMemberRequired, SingleObjectMixin, FormView):
    model = Course
    template_name = 'courses/non_members_book_course.html'
    context_object_name = 'course'
    form_class = NonMembersBookCourseForm

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Course.objects.filter(open_for_bookings=True, open_to_non_members=True)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'course': self.object,
            'user': self.request.user,
        })
        return kwargs

    def form_valid(self, form):
        attendee = form.save()
        if settings.SLACK_EVENTS_HREF:
            data = json.dumps({
                'icon_emoji': ':white_check_mark:',
                'text': '%s has registered for %s!' % (
                    attendee.archer,
                    attendee.course,
                )
            })
            try:
                requests.post(settings.SLACK_EVENTS_HREF, data=data)
            except Exception:
                pass
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('membership:overview')


class NonMembersPayment(MessageMixin, View):
    def get(self, request, *args, **kwargs):
        customer_id = self.request.user.customer_id or None
        membership_overview_url = reverse('membership:overview')
        attendees = Attendee.objects.filter(
            archer__user=self.request.user,
            member=False,
            paid=False,
            course__can_book_individual_sessions=False,
        )
        if not attendees:
            self.messages.error('You have no courses to pay for.')
            return redirect(membership_overview_url)
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'gbp',
                    'product_data': {
                        'name': '%s - %s' % (attendee, attendee.course),
                    },
                    'unit_amount': attendee.fee * 100,
                },
                'quantity': 1,
            } for attendee in attendees],
            mode='payment',
            customer=customer_id,
            customer_email=None if customer_id else self.request.user.email,
            customer_creation=None if customer_id else 'always',
            success_url=request.build_absolute_uri(membership_overview_url),
            cancel_url=request.build_absolute_uri(membership_overview_url),
        )
        intent = Checkout.objects.create(stripe_id=session.id, user=self.request.user)
        for attendee in attendees:
            intent.lineitemintent_set.create(item=attendee)
        return redirect(session.url, status_code=303)


class MinisInterestView(MessageMixin, CreateView):
    form_class = CourseInterestForm
    template_name = 'minis_interest_form.html'
    success_url = reverse_lazy('juniors')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['course_type'] = 'minis'
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        self.messages.success('Thanks for your interest! We will be in touch soon.')
        if settings.SLACK_EVENTS_HREF:
            data = json.dumps({
                'icon_emoji': ':wave:',
                'text': 'New minis course interest received for %s!\n%s' % (
                    form.cleaned_data['name'],
                    self.request.build_absolute_uri(
                        reverse(
                            'admin:courses_interest_change',
                            args=(form.instance.pk,),
                        )
                    ),
                )
            })
            try:
                requests.post(settings.SLACK_EVENTS_HREF, data=data)
            except Exception:
                pass
        return response
