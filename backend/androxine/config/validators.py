from typing import Any

from django.apps import apps
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class RestrictAmountValidator:
    '''
    Limits the number of foreign keys for a given field

    Args:
        model_app_name(str): name of model app
        model_name(str): model name
        lookup_field(str): name of the field to which the restriction is set
        limit(int): number of foreign keys

    '''

    def __init__(self, model_app_name: str, model_name: str, lookup_field: str, limit: int = 10) -> None:
        self.model_app_name = model_app_name
        self.model_name = model_name
        self.lookup_field = lookup_field
        self.limit = limit

    def __call__(self, value) -> Any:
        model = apps.get_model(
            app_label=self.model_app_name, model_name=self.model_name)
        if model.objects.filter(**{self.lookup_field: value}).count() >= self.limit:
            raise ValidationError(
                '{} already has maximal amount of refernces ({})'.format(
                    model.__name__, self.limit
                )
            )

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, RestrictAmountValidator)
            and (other.model_app_name == self.model_app_name)
            and (other.model_name == self.model_name)
            and (other.lookup_field == self.lookup_field)
            and (other.limit == self.limit)
        )
