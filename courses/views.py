import json

from django.conf import settings
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView, View
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse, reverse_lazy

from braces.views import MessageMixin
import requests
import stripe

from wallingford_castle.mixins import FullMemberRequired
from .models import Attendee, Course, CourseSignup, Summer2018Signup
from .forms import CourseSignupForm, MembersBookCourseForm, CourseInterestForm, Summer2018SignupForm


class Summer2018(TemplateView):
    template_name = 'courses/summer-2018.html'


class Summer2018Book(CreateView):
    template_name = 'courses/summer-2018-book.html'
    form_class = Summer2018SignupForm
    model = Summer2018Signup

    def get_success_url(self):
        return reverse('courses:summer-2018-payment', kwargs={'id': self.object.id})


class Summer2018Payment(DetailView):
    model = Summer2018Signup
    template_name = 'courses/summer-2018-payment.html'
    pk_url_kwarg = 'id'

    def get_cost(self, signup):
        return 5 * len(signup.dates)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if not self.object.paid:
            context['STRIPE_KEY'] = settings.STRIPE_KEY
            context['cost'] = self.get_cost(self.object)
        return context

    def post(self, request, *args, **kwargs):
        token = request.POST['stripeToken']
        signup = self.get_object()
        if signup.paid:
            return HttpResponseNotAllowed()
        stripe.Charge.create(
            amount=self.get_cost(signup) * 100,
            currency="GBP",
            description="Summer holiday archery",
            source=token,
            receipt_email=signup.email,
        )
        signup.paid = True
        signup.save()
        return HttpResponseRedirect(reverse('courses:summer-2018-payment', kwargs={'id': signup.id}))


class DGSSignup(MessageMixin, FormView):
    template_name = 'courses/dgs.html'
    form_class = CourseInterestForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['course_type'] = 'dgs'
        return kwargs

    def form_valid(self, form):
        form.save()
        self.messages.success('Thanks for your interest! We will be in touch soon.')
        if settings.SLACK_EVENTS_HREF:
            data = json.dumps({
                'icon_emoji': ':wave:',
                'text': 'New DGS course interest received for %s!\n%s' % (
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
        bookable_courses = Course.objects.filter(open_for_bookings=True, open_to_members=True)
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
