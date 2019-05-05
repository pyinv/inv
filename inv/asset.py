"""Classes for assets."""

from typing import Any, Mapping, Type, TypeVar, cast

from typesystem import Schema, String, ValidationError

from inv.types import AssetCode, Location

U = TypeVar('U', bound='Asset')


class Asset(Schema):
    """
    An individual item that exists in real space.

    An asset is labelled with a tracking label and can be moved between locations.
    """

    # Key attributes.
    code = AssetCode()
    location = Location()
    model = String(max_length=100)

    @classmethod
    def load(cls: Type[U], data: Mapping[Any, Any]) -> U:
        """Load an asset from a dictionary."""
        try:
            schema = cls.validate(data)
            return cast(U, schema)
        except ValidationError:
            raise
