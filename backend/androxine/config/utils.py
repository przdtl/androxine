import uuid
from ulid import ULID


def current_timestamp_ulid() -> uuid.UUID:
    ulid = ULID()
    return ulid.to_uuid()
