from django.urls import path

from . import api, views

app_name = 'coaching'

urlpatterns = [
    path('', views.GroupsOverview.as_view(), name='overview'),
    path('pay/', views.TrialPayment.as_view(), name='trial-payment'),
    path('trial/continue/<int:trial_pk>/', views.TrialContinue.as_view(), name='trial-continue'),
    path('<slug:group>/', views.GroupReport.as_view(), name='group-report'),
    path('upcoming/<slug:group>/', views.UpcomingGroupReport.as_view(), name='upcoming-group-report'),
    path('<slug:group>/sessions/', views.GroupSchedule.as_view(), name='group-schedule'),
    path('upcoming/<slug:group>/sessions/', views.UpcomingGroupSchedule.as_view(), name='upcoming-group-schedule'),

    path('<int:archer_id>/event-plan/', views.EventPlan.as_view(), name='event-plan'),
    path('<int:archer_id>/upcoming/event-plan/', views.NextEventPlan.as_view(), name='next-event-plan'),
]

coaching_api_urlpatterns = [
    path('plan/<int:plan_id>/', api.plan_info, name='plan-info'),
]
