from django.urls import path
from .resources import category, wallet, log

urlpatterns = [
    path('logs', log.log_root),
    path('logs/<int:id>', log.log_by_id),
    path('categories', category.category_root),
    path('categories/<int:id>', category.category_by_id),
    path('wallets', wallet.wallet_root),
    path('wallets/<int:id>', wallet.wallet_by_id),
]
