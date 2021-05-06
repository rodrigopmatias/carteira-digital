from base.resources.ping import ping
from base.resources.health import health
from django.urls import path

urlpatterns = [
    path('health', health),
    path('ping', ping)
]
