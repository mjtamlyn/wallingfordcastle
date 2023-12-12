from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from .models import Tournament


def tournament_info(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    return JsonResponse({
        'tournament': {
            'id': tournament.pk,
            'name': str(tournament),
            'baseUrl': reverse('tournaments:tournament-detail', kwargs={'tournament_slug': tournament.slug}),
            'entryIsOpen': tournament.entry_is_open,
        },
    })
