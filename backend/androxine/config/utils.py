import uuid
from ulid import ULID
from typing import Optional

from django.http import QueryDict
from django.core.exceptions import ValidationError

from rest_framework.generics import get_object_or_404


def current_timestamp_ulid() -> uuid.UUID:
    ulid = ULID()
    return ulid.to_uuid()


def ordinal_number_validation(obj, fieldname, **filters):
    ordinal_number = getattr(obj, fieldname)
    error_text = 'incorrect order'

    if ordinal_number == 1:
        try:
            obj.__class__.objects.get(**{fieldname: ordinal_number}, **filters)
        except obj.__class__.DoesNotExist:
            return
        else:
            raise ValidationError(
                {fieldname: error_text}
            )

    try:
        obj.__class__.objects.get(**{fieldname: ordinal_number - 1}, **filters)
    except obj.__class__.DoesNotExist:
        raise ValidationError(
            {fieldname: error_text}
        )
    try:
        obj.__class__.objects.get(**{fieldname: ordinal_number}, **filters)
    except obj.__class__.DoesNotExist:
        return
    else:
        raise ValidationError(
            {fieldname: error_text}
        )


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
    def __init__(self, request_data) -> None:
        self.request_data = request_data
        self.is_query_dict = isinstance(self.request_data, QueryDict)

    def __enter__(self) -> None:
        if self.is_query_dict:
            self.request_data._mutable = True

    def __exit__(self) -> None:
        if self.is_query_dict:
            self.request_data._mutable = False
