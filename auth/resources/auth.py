import jwt
import json

from datetime import datetime, timedelta
from django.http.response import HttpResponseNotAllowed, JsonResponse
from django.conf import settings
from django.apps import apps


def register(request):
    status = 501
    result = {
        "message": "method not implemented"
    }

    if request.method == 'POST':
        try:
            UserModel = apps.get_model(getattr(settings, 'AUTH_USER_MODEL'))
            payload = json.loads(request.body)
            password = payload.pop('password')
            confirm_password = payload.pop('confirm_password')

            if password == confirm_password:
                user = UserModel(**payload)
                user.is_active = not UserModel.objects.filter(is_active=True).exists()
                user.is_superuser = not UserModel.objects.filter(is_active=True, is_superuser=True).exists()
                user.set_password(password)
                user.save()

                status = 201
                result = {
                    'user_id': user.id
                }
            else:
                status = 400
                result = {
                    "message": 'password not confirmed'
                }
        except Exception as e:
            status = 502
            result = {
                "message": str(e)
            }
    else:
        return HttpResponseNotAllowed(
            permitted_methods=['POST']
        )

    return JsonResponse(
        result,
        status=status
    )

def token(request):
    status = 501
    result = {
        "message": "method not implemented"
    }

    if request.method == 'POST':
        try:
            UserModel = apps.get_model(getattr(settings, 'AUTH_USER_MODEL'))
            payload = json.loads(request.body)
            password = payload.pop('password')
            user = UserModel.objects.get(email=payload.pop('email'))

            if user.is_active and user.check_password(password):
                status = 200
                result = {
                    'token': jwt.encode(
                        {
                            'user_id': user.pk,
                            "iat": datetime.utcnow(),
                            "exp": datetime.utcnow() + timedelta(minutes=15)
                        },
                        'secr3t',
                        algorithm="HS256"
                    )
                }
            else:
                status = 401
                result = {
                    "message": 'user or password not match'
                }
        except Exception as e:
            status = 401
            result = {
                "message": 'user or password not match'
            }
    else:
        return HttpResponseNotAllowed(
            permitted_methods=['POST']
        )

    return JsonResponse(
        result,
        status=status
    )

def renew_token(request):
    status = 501
    result = {
        "message": "method not implemented"
    }

    if request.method == 'GET':
        user = getattr(request, 'user', None)

        if user and user.is_active:
            status = 200
            result = {
                'token': jwt.encode(
                    {
                        'user_id': user.pk,
                        "iat": datetime.utcnow(),
                        "exp": datetime.utcnow() + timedelta(minutes=15)
                    },
                    'secr3t',
                    algorithm="HS256"
                )
            }
    else:
        return HttpResponseNotAllowed(
            permitted_methods=['GET']
        )

    return JsonResponse(
        result,
        status=status
    )

def me(request):
    status = 401
    result = {
        "message": "user not authorized"
    }
    user = getattr(request, 'user', None)

    if user and user.is_active:
        status = 200
        result = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'id': user.id,
        }

    return JsonResponse(
        result,
        status=status
    )