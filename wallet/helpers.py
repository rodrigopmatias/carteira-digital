from django.http.request import HttpRequest
from django.db import models


def owner_by_payload(request: HttpRequest, payload: dict) -> dict:
    user = getattr(request, 'user', None)

    if user and user.is_active:
        payload.update(owner_id=user.pk)

    return payload


def queryset_by_owner(Model: models.Model) -> dict:
    def _queryset_by_owner(request):
        user = getattr(request, 'user', None)

        if user and user.is_active:
            return Model.objects.filter(owner=user)

        return Model.objects.none()
    return _queryset_by_owner
