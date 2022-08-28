from django.urls import include, path

from . import views

app_name = 'tournaments'

tournament_patterns = [
    path('', views.TournamentDetail.as_view(), name='tournament-detail'),
    path('register/', views.TournamentRegistration.as_view(), name='register'),
    path('enter/', views.EntryCreate.as_view(), name='enter'),
    path('entry/<int:pk>/', views.EntryUpdate.as_view(), name='entry-update'),
    path('enter/<int:pk>/delete/', views.EntryDelete.as_view(), name='entry-delete'),
    path('pay/', views.Pay.as_view(), name='pay'),
    path('pay/success/', views.PaymentSuccess.as_view(), name='pay-success'),
]

urlpatterns = [
    path('', views.TournamentList.as_view(), name='home'),
    path('series/<series_slug>/', views.SeriesDetail.as_view(), name='series-detail'),
    path('series/<series_slug>/register/', views.SeriesRegistration.as_view(), name='series-register'),
    path('series/<series_slug>/enter/', views.SeriesEntryCreate.as_view(), name='series-enter'),
    path('<tournament_slug>/', include(tournament_patterns)),
]
