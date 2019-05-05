"""Asset code."""

from typing import Any, Callable, Optional

from typesystem import String


class AssetCode(String):
    """An asset code identifies an asset uniquely."""

    errors = {
        "checksum": "Must have a valid checksum.",
        "prefix_required": "Must have the specified prefix.",
    }

    def __init__(
            self,
            *,
            prefix: Optional[str] = None,
            prefix_required: bool = True,
            checksum: Optional[Callable[[str], bool]] = None,
            max_length: Optional[int] = None,
            **kwargs: Any,
    ):
        self.prefix = prefix
        self.prefix_required = prefix_required
        self.checksum = checksum

        if self.prefix:
            # Extend the maximum length if we have a prefix
            if max_length is not None:
                max_length += len(self.prefix)

        # Todo: Fix this mess.
        if max_length is not None:
            super().__init__(
                max_length=max_length,
                **kwargs,
            )
        else:
            super().__init__(**kwargs)

    def validate(self, value: Any, *, strict: bool = False) -> Any:
        """Validate the value."""
        # Check if it's a string in the superclass
        value = super().validate(value, strict=strict)

        # Asset Code Prefixes.
        if self.prefix is not None:

            prefix_guess = value[:len(self.prefix)]

            if prefix_guess == self.prefix:
                # We have a valid prefix. Remove it.
                value = value[len(self.prefix):]
            else:
                if self.prefix_required:
                    raise self.validation_error("prefix_required")

        # Convert to upper case
        value = value.upper()

        # Checksum
        if self.checksum is not None:
            if not self.checksum(value):
                raise self.validation_error("checksum")

        return value
