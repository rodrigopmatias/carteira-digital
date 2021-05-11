from wallet.helpers import queryset_by_owner
from helpers.serializer import BaseSerializer
from helpers.restfy import make_authorized_rest
from wallet.models import Log
from django.db import models


class LogSerializer(BaseSerializer):

    _model = Log

    @classmethod
    def encode(cls, instance: models.Model) -> dict:
        result = super().encode(instance)

        result.update(
            title=instance.title,
            value=float(instance.value or 0),
            when=str(instance.when) if instance.when else None,
            schedule=str(instance.schedule) if instance.schedule else None,
            wallet_id=instance.wallet.id,
            category_id=instance.category.id,
        )

        return result


def queryset(request):
    user = getattr(request, 'user', None)

    if user and user.is_active:
        return Log.objects.filter(wallet__owner=user)

    return Log.objects.none()


log_root, log_by_id = make_authorized_rest(
    LogSerializer,
    queryset=queryset
)