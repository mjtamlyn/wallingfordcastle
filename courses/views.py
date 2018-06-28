from django.conf import settings
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.views.generic import CreateView, DetailView, TemplateView
from django.urls import reverse

import stripe

from .models import CourseSignup, Summer2018Signup
from .forms import CourseSignupForm, Summer2018SignupForm


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
