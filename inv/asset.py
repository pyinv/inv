"""Classes for assets."""

from typesystem import Schema, String


class Asset(Schema):
    """
    An individual item that exists in real space.

    An asset is labelled with a tracking label and can be moved between locations.
    """

    # Key attributes.
    code = String(max_length=100)
    model = String(max_length=100)
    location = String(max_length=100)

    def __init__(self, *, code: String, model: String, location: String) -> None:
        self.code = code
        self.model = model
        self.location = location
