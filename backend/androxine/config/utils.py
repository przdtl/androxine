import uuid

from ulid import ULID
from typing import Any, Optional, Self, Iterable

from django.apps import apps
from django.conf import settings
from django.http import QueryDict
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.decorators import method_decorator

from rest_framework.generics import get_object_or_404


def current_timestamp_ulid() -> uuid.UUID:
    ulid = ULID()
    return ulid.to_uuid()


class CustomGetObjectMixin:
    lookup_fields: dict = {}
    shadow_user_lookup_field: Optional[str] = None

    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {}

        for lookup_field, lookup_url_kwarg in self.lookup_fields.items():
            assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
            )
            filter_kwargs.update({lookup_field: self.kwargs[lookup_url_kwarg]})

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if lookup_url_kwarg in self.kwargs:
            filter_kwargs.update({
                self.lookup_field: self.kwargs[lookup_url_kwarg]
            })
        if self.shadow_user_lookup_field:
            filter_kwargs.update({
                self.shadow_user_lookup_field: self.request.user.pk
            })
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)

        return obj


class UpdateRequestManager:
    def __init__(self, request_data) -> Self:
        self.request_data = request_data
        self.is_query_dict = isinstance(self.request_data, QueryDict)

    def __enter__(self) -> None:
        if self.is_query_dict:
            self.request_data._mutable = True

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        if self.is_query_dict:
            self.request_data._mutable = False


@deconstructible
class RestrictAmountValidator:
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


def delete_cache(key_prefix: str):
    """
    Delete all cache keys with the given prefix.
    """
    keys_pattern = f"*.{key_prefix}_*.{settings.LANGUAGE_CODE}.{settings.TIME_ZONE}"
    cache.delete_pattern(keys_pattern)


def methods_decorator(decorator, names: Iterable[str]):
    def _dec(obj):
        for name in names:
            decorator_obj = method_decorator(decorator, name)
            obj = decorator_obj(obj)

        return obj

    return _dec
