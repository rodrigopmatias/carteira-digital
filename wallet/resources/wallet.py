from wallet.models import Wallet
from helpers.serializer import BaseSerializer
from helpers.restfy import make_rest
from django.http.request import HttpRequest
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


def catetory_prepare_payload(request: HttpRequest, payload: dict) -> dict:
    payload.update(owner_id=1)
    return payload

wallet_root, wallet_by_id = make_rest(
    WalletSerializer,
    prepare_payload=catetory_prepare_payload
)