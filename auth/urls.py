from django.urls import path
from .resources import auth

urlpatterns = [
    path('register', auth.register),
    path('token', auth.token),
    path('me', auth.me),
]
