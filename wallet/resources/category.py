from wallet.helpers import owner_by_payload, queryset_by_owner
from wallet.models import Category
from helpers.serializer import BaseSerializer
from helpers.restfy import make_authorized_rest
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


category_root, category_by_id = make_authorized_rest(
    CategorySerializer,
    prepare_payload=owner_by_payload,
    queryset=queryset_by_owner(Category)
)
