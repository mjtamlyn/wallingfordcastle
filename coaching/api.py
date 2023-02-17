from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404

from .models import ArcherSeason


def plan_info(request, plan_id):
    plan = get_object_or_404(ArcherSeason, pk=plan_id)
    archer = plan.archer
    if archer.user_id != request.user.pk and request.user not in archer.managing_users.all():
        raise Http404
    response = {
        'archer': str(plan.archer),
        'ageGroup': plan.archer.age_group,
        'season': str(plan.season),
        'targetClassification': {
            'id': plan.target_classification,
            'name': plan.get_target_classification_display(),
        },
        'personalisedTargetComments': plan.personalised_target_comments,
    }
    return JsonResponse(response)
