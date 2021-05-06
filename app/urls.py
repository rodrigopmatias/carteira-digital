from django.urls import path, include

urlpatterns = [
    path('_/', include('base.urls')),
    path('auth/', include('auth.urls')),
    path('', include('wallet.urls'))
]
