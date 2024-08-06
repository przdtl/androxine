import uuid
from ulid import ULID

from django.core.exceptions import ValidationError


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
