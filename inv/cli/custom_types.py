"""Custom Click ParamTypes."""
import re
from typing import Optional

import click

from inv.asset_code import Damm32AssetCode


class Damm32AssetCodeParamType(click.ParamType):
    """ParamType for Damm32 Asset Codes."""

    name = "asset_code"

    def __init__(self, org: str):
        self.org = org

    def convert(
            self,
            value: str,
            param: Optional[click.Parameter],
            ctx: Optional[click.Context],
    ) -> str:
        """Convert."""

        # Check the format, and convert to internal if needed.
        FULL_REGEX = f"^{self.org}-([A-Z2-7]{{3}})-([A-Z2-7]{{3}})$"

        match = re.match(FULL_REGEX, value)

        if match is None:
            self.fail("asset code in wrong format")

        value = match.group(1) + match.group(2)

        # Prefix is unused here, so we use AA
        d32ac = Damm32AssetCode(self.org, "AA")

        if not d32ac.verify(value):
            self.fail(f"failed to verify asset code: {value}")

        return value


DAMM32 = Damm32AssetCodeParamType
