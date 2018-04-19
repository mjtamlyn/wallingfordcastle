from django.conf import settings
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.views.generic import CreateView, DetailView
from django.urls import reverse

import stripe

from .models import CourseSignup
from .forms import CourseSignupForm



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
            amount=2000,
            currency="GBP",
            description="Didcot Girls School Archery Club",
            source=token,
            receipt_email=signup.email,
        )
        signup.paid = True
        signup.save()
        return HttpResponseRedirect(reverse('courses:dgs-payment', kwargs={'id': signup.id}))
