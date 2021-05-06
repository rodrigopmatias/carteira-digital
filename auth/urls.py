from django.urls import path
from .resources import auth

urlpatterns = [
    path('register', auth.register),
    path('token', auth.token),
    path('renew-token', auth.renew_token),
    path('me', auth.me),
]
