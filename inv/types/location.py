"""Asset Location."""

from typing import Any

from typesystem import String

# The format for location strings, e.g "a_site/a_location/large_camera-6yh9jf"
LOCATION_FORMAT = "^((?:[a-z_]+/)*)([a-z_]+)-([a-z0-9]+)$"


class Location(String):
    """A physical location where assets can be stored."""

    def __init__(
            self,
            **kwargs: Any,
    ):
        if 'pattern' in kwargs.keys():
            raise ValueError("The regex for a location cannot be redefined.")

        super().__init__(
            pattern=LOCATION_FORMAT,
            **kwargs,
        )

    def validate(self, value: Any, *, strict: bool = False) -> Any:
        """Validate the value."""
        # Check if it's a string in the superclass
        value = super().validate(value, strict=strict)

        return value
