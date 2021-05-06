
from django.http.response import JsonResponse


def health(request):
    return JsonResponse(
        {
            "message": 'its is alive!!!'
        },
        status=200
    )