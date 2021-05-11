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


log_root, log_by_id = make_authorized_rest(
    LogSerializer
)