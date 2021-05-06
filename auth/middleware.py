import jwt
import re

from django.conf import settings
from django.apps import apps

class JWTAuthorizationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        authorization = request.headers.get('authorization', None)

        if authorization:
            result = re.match('^(JWT|Bearer) (.*)', authorization)
            if result:
                method, token = result.groups()
                if method in ('JWT', 'Bearer'):
                    try:
                        UserModel = apps.get_model(getattr(settings, 'AUTH_USER_MODEL'))

                        payload = jwt.decode(token, key='secr3t', algorithms=["HS256"])
                        request.user = UserModel.objects.get(pk=payload.get('user_id'))
                    except Exception:
                        pass

        return self.get_response(request)