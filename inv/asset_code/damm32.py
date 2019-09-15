"""Damm32 based code."""

from random import choice
from re import compile
from typing import ClassVar

from .abstract import AbstractAssetCode

try:
    from damm32 import Damm32
except ImportError:  # pragma: nocover
    print("Unable to import damm32. Make sure to install it as an extra.")
    exit(1)

ALPHABET_REGEX = "A-Z2-7"
ORG_REGEX = compile("^[A-Z]{3}$")
PREFIX_REGEX = compile(f"^[{ALPHABET_REGEX}]{{2}}$")


class Damm32AssetCode(AbstractAssetCode):
    """Damm32-based Asset Code."""

    name: ClassVar[str] = "Damm32 Verified Asset Code"
    format_regex: ClassVar[str] = f"^[{ALPHABET_REGEX}]{{6}}$"

    def __init__(
            self,
            org: str,
            prefix: str,
    ):
        if ORG_REGEX.match(org) is None:
            raise ValueError(
                "Organisation prefix for Asset Code can only contain A-Z",
            )
        if PREFIX_REGEX.match(prefix) is None:
            raise ValueError(
                "Prefix for asset code must be 2 long and use valid chars",
            )
        self._org = org
        self._prefix = prefix

        self._damm32 = Damm32()

    def _generate_code(self) -> str:
        """
        Generate an individual asset code.

        :return: An unformatted asset code.
        """
        code = "" + self._prefix
        for i in range(0, 3):
            code += choice(Damm32.ALPHABET)

        code += self._damm32.calculate(self._org + code)
        return code

    def _verify_code(self, candidate: str) -> bool:
        """Verify whether a string is a valid asset code."""
        return self._damm32.verify(self._org + candidate.upper())
