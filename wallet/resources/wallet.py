from wallet.helpers import owner_by_payload
from wallet.models import Wallet
from helpers.serializer import BaseSerializer
from helpers.restfy import make_authorized_rest
from django.db import models


class WalletSerializer(BaseSerializer):

    _model = Wallet

    @classmethod
    def encode(cls, instance: models.Model) -> dict:
        result = super().encode(instance)

        result.update(
            name=instance.name
        )

        return result


wallet_root, wallet_by_id = make_authorized_rest(
    WalletSerializer,
    prepare_payload=owner_by_payload
)