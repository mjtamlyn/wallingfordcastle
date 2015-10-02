from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import password_reset_confirm
from django.core.urlresolvers import reverse_lazy

from . import views
from .forms import RegisterForm


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^membership-interest/$', views.MembershipInterestView.as_view(), name='membership-interest'),
    url(r'^beginners-course/$', views.BeginnersCourseView.as_view(), name='beginners-course'),

    url(r'^members/', include('membership.urls', namespace='membership')),
    # TODO: Password reset flow templates
    # TODO: Style header links
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/register/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        password_reset_confirm, {
            'set_password_form': RegisterForm,
            'template_name': 'registration/register.html',
            'post_reset_redirect': reverse_lazy('membership:overview'),
        }, name='register'),
    url(r'^admin/', include(admin.site.urls)),
)
