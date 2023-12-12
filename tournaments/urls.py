from django.urls import include, path, re_path

from . import api, views

app_name = 'tournaments'

tournament_patterns = [
    path('', views.TournamentDetail.as_view(), name='tournament-detail-old'),
    path('register/', views.TournamentRegistration.as_view(), name='register'),
    path('enter/', views.EntryCreate.as_view(), name='enter'),
    path('entry/<int:pk>/', views.EntryUpdate.as_view(), name='entry-update'),
    path('enter/<int:pk>/delete/', views.EntryDelete.as_view(), name='entry-delete'),
    path('pay/', views.Pay.as_view(), name='pay'),
    path('pay/success/', views.PaymentSuccess.as_view(), name='pay-success'),
]

series_patterns = [
    path('', views.SeriesDetail.as_view(), name='series-detail'),
    path('register/', views.SeriesRegistration.as_view(), name='series-register'),
    path('enter/', views.SeriesEntryCreate.as_view(), name='series-enter'),
    path('pay/', views.SeriesPay.as_view(), name='series-pay'),
    path('pay/success/', views.SeriesPaymentSuccess.as_view(), name='series-pay-success'),
]

tournaments_api_urlpatterns = [
    path('<int:tournament_id>/', api.tournament_info, name='tournament-info'),
]

urlpatterns = [
    path('', views.TournamentList.as_view(), name='home'),
    path('series/<series_slug>/', include(series_patterns)),
    re_path('^(?P<tournament_slug>[a-z0-9]+(?:-[a-z0-9]+)*)/',
            views.TournamentDetail.as_view(), name='tournament-detail'),
    path('old/<tournament_slug>/', include(tournament_patterns)),
]
