from django.contrib import admin
from django.contrib.auth.views import password_reset_confirm
from django.urls import include, path, reverse_lazy, re_path

from . import views
from .forms import RegisterForm


admin.autodiscover()


urlpatterns = [
    re_path(r'^$', views.HomeView.as_view(), name='home'),
    re_path(r'^membership-interest/$', views.MembershipInterestView.as_view(), name='membership-interest'),
    re_path(r'^beginners/', include('beginners.urls', namespace='beginners')),
    re_path(r'^members/', include('membership.urls', namespace='membership')),
    re_path(r'^members/events/', include('events.urls', namespace='events')),
    re_path(r'^tournaments/', include('tournaments.urls', namespace='tournaments')),
    # TODO: Style header links
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/<uidb64>/<token>/',
        password_reset_confirm, {
            'set_password_form': RegisterForm,
            'template_name': 'registration/register.html',
            'post_reset_redirect': reverse_lazy('membership:overview'),
        }, name='register'),
    re_path(r'^admin/', admin.site.urls),
]
