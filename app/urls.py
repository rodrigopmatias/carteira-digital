from django.urls import path, include

urlpatterns = [
    path('_/', include('base.urls')),
    path('', include('wallet.urls'))
]
