from django.conf import settings
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse

import stripe

from wallingford_castle.mixins import FullMemberRequired
from .models import Course, CourseSignup, Summer2018Signup
from .forms import CourseSignupForm, MembersBookCourseForm, Summer2018SignupForm


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


class DGSSignup(CreateView):
    template_name = 'courses/dgs.html'
    form_class = CourseSignupForm
    model = CourseSignup

    def get_success_url(self):
        return reverse('courses:dgs-payment', kwargs={'id': self.object.id})


class DGSPayment(DetailView):
    model = CourseSignup
    template_name = 'courses/payment.html'
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if not self.object.paid:
            context['STRIPE_KEY'] = settings.STRIPE_KEY
        return context

    def post(self, request, *args, **kwargs):
        token = request.POST['stripeToken']
        signup = self.get_object()
        if signup.paid:
            return HttpResponseNotAllowed()
        stripe.Charge.create(
            amount=5500,
            currency="GBP",
            description="Didcot Girls School Archery Club",
            source=token,
            receipt_email=signup.email,
        )
        signup.paid = True
        signup.save()
        return HttpResponseRedirect(reverse('courses:dgs-payment', kwargs={'id': signup.id}))


class MembersCourseList(FullMemberRequired, ListView):
    model = Course
    template_name = 'courses/members_course_list.html'

    def get_queryset(self):
        # TODO
        # Exclude courses which aren't open, or available to members
        # Maybe order by start date?
        bookable_courses = Course.objects.all()
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
        # TODO
        # Exclude courses which aren't open, or available to members
        return Course.objects.all()

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
