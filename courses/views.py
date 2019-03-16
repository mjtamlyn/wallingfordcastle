import json

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Prefetch, Q
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView, View
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse, reverse_lazy

from braces.views import MessageMixin
import requests
import stripe

from wallingford_castle.forms import DirectRegisterForm
from wallingford_castle.mixins import FullMemberRequired
from wallingford_castle.models import Archer
from membership.models import Member
from .models import Attendee, Course, Session, Summer2018Signup
from .forms import MembersBookCourseForm, CourseInterestForm, Summer2018SignupForm, NonMembersBookCourseForm, SessionBookingForm


class Holidays(TemplateView):
    template_name = 'courses/holidays.html'


class HolidaysBook(MessageMixin, TemplateView):
    template_name = 'courses/holidays-book.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.course = Course.objects.get(can_book_individual_sessions=True, open_for_bookings=True)
        except Course.DoesNotExist:
            self.messages.error('Bookings are not currently open, sorry. Please contact us for more information.')
            return HttpResponseRedirect(reverse('courses:holidays'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_anonymous:
            context.setdefault('login_form', AuthenticationForm())
            context.setdefault('register_form', DirectRegisterForm())
        else:
            context['members'] = Member.objects.managed_by(self.request.user).filter(archer__age='junior').select_related('archer')
            member_archers = [member.archer_id for member in context['members']]

            for member in context['members']:
                archer = member.archer
                try:
                    member.archer.attendee = archer.attendee_set.get(course=self.course)
                    member.archer.sessions_booked = archer.attendee.session_set.order_by('session__start_time')
                    member.archer.booking_form = SessionBookingForm(course=self.course, booked=archer.sessions_booked, prefix=archer.pk)
                except Attendee.DoesNotExist:
                    member.archer.attendee = None
                    member.archer.booking_form = SessionBookingForm(course=self.course, prefix=archer.pk)

            other_archers = Archer.objects.filter(
                Q(user=self.request.user) | Q(managing_users=self.request.user),
                age='junior',
            ).exclude(id__in=member_archers)
            context['archers'] = other_archers

            for archer in context['archers']:
                try:
                    archer.attendee = archer.attendee_set.get(course=self.course)
                    archer.sessions_booked = archer.attendee.session_set.order_by('session__start_time')
                    archer.booking_form = SessionBookingForm(course=self.course, booked=archer.sessions_booked, prefix=archer.pk)
                except Attendee.DoesNotExist:
                    archer.attendee = None
                    archer.booking_form = SessionBookingForm(course=self.course, prefix=archer.pk)

            context.setdefault('new_archer_form', CourseInterestForm(initial={'contact_email': self.request.user.email}, course_type='holidays'))
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
                interest = form.save()
                interest.convert_to_archer(self.request.user)
                return self.get(request, *args, **kwargs)
            else:
                context['new_archer_form'] = form
        elif form == 'booking':
            archer_id = request.POST['archer']
            form = SessionBookingForm(data=request.POST, course=self.course, prefix=archer_id)
            if form.is_valid():
                form.save(archer_id=archer_id)
                return self.get(request, *args, **kwargs)
        return self.render_to_response(context=self.get_context_data(**context))


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
        )
        for course in bookable_courses:
            user = self.request.user
            course.registered_members = course.attendee_set.filter(archer__user=user) | course.attendee_set.filter(archer__managing_users=user)
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
            course.registered_archers = course.attendee_set.filter(archer__user=user) | course.attendee_set.filter(archer__managing_users=user)
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
        return reverse('courses:non-members-course-list')


class NonMembersPayment(MessageMixin, View):
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
        attendees = Attendee.objects.filter(archer__user=self.request.user, member=False, paid=False)
        amount = sum(attendee.fee for attendee in attendees)
        description = '; '.join('%s - %s' % (attendee.archer, attendee.course) for attendee in attendees)
        stripe.Charge.create(
            amount=amount * 100,
            currency='gbp',
            customer=customer.id,
            description=description,
        )
        attendees.update(paid=True)
        self.messages.success('Thanks! You will receive a confirmation email soon.')
        return HttpResponseRedirect(reverse('membership:overview'))


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
