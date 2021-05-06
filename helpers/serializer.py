from django.db import models


class BaseSerializer:

    _model : models.Model

    @classmethod
    def model_class(cls):
        return cls._model
        
    @classmethod
    def encode(cls, instance: models.Model) -> dict:
        return {
            'pk': instance.pk,
            'description': str(instance)
        }

    @classmethod
    def decode(cls, payload: dict) -> models.Model:
        return cls._model(**payload)