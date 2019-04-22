from django.contrib import admin
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import include, path, reverse_lazy, re_path

from . import views
from .forms import RegisterForm


admin.autodiscover()


urlpatterns = [
    re_path(r'^$', views.HomeView.as_view(), name='home'),
    re_path(r'^join/$', views.Join.as_view(), name='join'),
    re_path(r'^juniors/$', views.Juniors.as_view(), name='juniors'),
    re_path(r'^membership-interest/$', views.MembershipInterestView.as_view(), name='membership-interest'),
    re_path(r'^beginners/', include('beginners.urls', namespace='beginners')),
    re_path(r'^members/', include('membership.urls', namespace='membership')),
    re_path(r'^members/events/', include('events.urls', namespace='events')),
    re_path(r'^tournaments/', include('tournaments.urls', namespace='tournaments')),
    re_path(r'^events/', include('bookings.urls', namespace='bookings')),
    re_path(r'^venues/$', views.Venues.as_view(), name='venues'),
    # TODO: Style header links
    path('accounts/login/', views.Login.as_view(), name='login'),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            form_class=RegisterForm,
            template_name='registration/register.html',
            success_url=reverse_lazy('membership:overview'),
        ), name='register'),
    re_path(r'^admin/', admin.site.urls),
    path('', include('courses.urls', namespace='courses')),
]
