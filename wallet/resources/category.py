from wallet.models import Category
from helpers.serializer import BaseSerializer
from helpers.restfy import make_rest
from django.http.request import HttpRequest
from django.db import models


class CategorySerializer(BaseSerializer):

    _model = Category

    @classmethod
    def encode(cls, instance: models.Model) -> dict:
        result = super().encode(instance)

        result.update(
            title=instance.title
        )

        return result


def catetory_prepare_payload(request: HttpRequest, payload: dict) -> dict:
    payload.update(owner_id=1)
    return payload

category_root, category_by_id = make_rest(
    CategorySerializer,
    prepare_payload=catetory_prepare_payload
)