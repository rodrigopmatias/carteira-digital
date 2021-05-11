from django.http.request import HttpRequest

def owner_by_payload(request: HttpRequest, payload: dict) -> dict:
    user = getattr(request, 'user', None)

    if user and user.is_active:
        payload.update(owner_id=user.pk)

    return payload
