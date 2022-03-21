from django.urls import path

from . import views

app_name = 'coaching'

urlpatterns = [
    path('', views.GroupsOverview.as_view(), name='overview'),
    path('pay/', views.TrialPayment.as_view(), name='trial-payment'),
    path('<slug:group>/', views.GroupReport.as_view(), name='group-report'),
    path('upcoming/<slug:group>/', views.UpcomingGroupReport.as_view(), name='upcoming-group-report'),
    path('<slug:group>/sessions/', views.GroupSchedule.as_view(), name='group-schedule'),
    path('upcoming/<slug:group>/sessions/', views.UpcomingGroupSchedule.as_view(), name='upcoming-group-schedule'),
]
