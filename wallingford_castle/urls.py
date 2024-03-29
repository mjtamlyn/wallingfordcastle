from django.contrib import admin
from django.contrib.auth.views import (
    PasswordResetConfirmView, PasswordResetView,
)
from django.urls import include, path, reverse_lazy

from coaching.urls import coaching_api_urlpatterns
from events.urls import range_api_urlpatterns

from . import views
from .forms import RegisterForm, SendgridPasswordResetForm

admin.autodiscover()


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('join/', views.Join.as_view(), name='join'),
    path('juniors/', views.Juniors.as_view(), name='juniors'),
    path('membership-interest/', views.MembershipInterestView.as_view(), name='membership-interest'),
    path('beginners/', include('beginners.urls', namespace='beginners')),
    path('coaching/', include('coaching.urls', namespace='coaching')),
    path('api/coaching/', include((coaching_api_urlpatterns, 'coaching-api'))),
    path('members/', include('membership.urls', namespace='membership')),
    path('members/events/', include('events.urls', namespace='events')),
    path('api/range/', include(range_api_urlpatterns)),
    path('tournaments/', include('tournaments.urls', namespace='tournaments')),
    path('events/', include('bookings.urls', namespace='bookings')),
    path('venues/', include('venues.urls', namespace='venues')),
    # TODO: Style header links
    path('accounts/login/', views.Login.as_view(), name='login'),
    path('accounts/password_reset/', PasswordResetView.as_view(
        form_class=SendgridPasswordResetForm,
    ), name='password_reset'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        form_class=RegisterForm,
        template_name='registration/register.html',
        success_url=reverse_lazy('membership:overview'),
    ), name='register'),
    path('admin/', admin.site.urls),
    path('webhooks/stripe/', include('payments.urls', namespace='payments')),
    path('', include('courses.urls', namespace='courses')),
]
