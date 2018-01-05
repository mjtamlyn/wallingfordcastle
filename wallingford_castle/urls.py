from django.contrib import admin
from django.contrib.auth.views import password_reset_confirm
from django.urls import include, reverse_lazy, re_path

from . import views
from .forms import RegisterForm


admin.autodiscover()


urlpatterns = [
    re_path(r'^$', views.HomeView.as_view(), name='home'),
    re_path(r'^membership-interest/$', views.MembershipInterestView.as_view(), name='membership-interest'),
    re_path(r'^beginners/', include('beginners.urls', namespace='beginners')),
    re_path(r'^members/', include('membership.urls', namespace='membership')),
    re_path(r'^tournaments/', include('tournaments.urls', namespace='tournaments')),
    # TODO: Style header links
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'^accounts/register/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        password_reset_confirm, {
            'set_password_form': RegisterForm,
            'template_name': 'registration/register.html',
            'post_reset_redirect': reverse_lazy('membership:overview'),
        }, name='register'),
    re_path(r'^admin/', admin.site.urls),
]
