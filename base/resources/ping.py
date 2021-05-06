from django.http.response import JsonResponse

def ping(request):
    return JsonResponse(
        {
            "message": "pong"
        },
        status=200
    )