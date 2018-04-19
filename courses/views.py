from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy

from .forms import CourseSignupForm



class DGSSignup(FormView):
    template_name = 'courses/dgs.html'
    form_class = CourseSignupForm
    success_url = reverse_lazy('courses:dgs-payment')


class DGSPayment(TemplateView):
    template_name = 'courses/payment.html'
