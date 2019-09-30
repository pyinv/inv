"""Custom Click ParamTypes."""
import re
from typing import Optional

import click

from inv.asset_manufacturer import AssetManufacturer
from inv.cli.env import get_inv


class AssetCodeParamType(click.ParamType):
    """ParamType for Damm32 Asset Codes."""

    name = "asset_code"

    def convert(
            self,
            value: str,
            _: Optional[click.Parameter],
            ctx: Optional[click.Context],
    ) -> str:
        """Convert."""
        inv = get_inv()

        # Check the format, and convert to internal if needed.
        FULL_REGEX = f"^{inv.org}-([A-Z2-7]{{3}})-([A-Z2-7]{{3}})$"

        match = re.match(FULL_REGEX, value)

        if match is None:
            self.fail("asset code in wrong format")
            return ""  # Unreachable
        else:
            value = match.group(1) + match.group(2)

            if not inv.asset_code.verify(value):
                self.fail(f"failed to verify asset code: {value}")

            return value


class AssetManufacturerParamType(click.ParamType):
    """ParamType for Manufacturer."""

    name = "manufacturer"

    def convert(
            self,
            value: str,
            _: Optional[click.Parameter],
            ctx: Optional[click.Context],
    ) -> AssetManufacturer:
        """Convert."""
        inv = get_inv()

        name_format = value.lower().replace(" ", "_").replace("-", "_")
        name_format = re.sub('[^a-z0-9_]+', '', name_format)

        try:
            man = inv.get_manufacturer(name_format)
        except ValueError:
            self.fail("Unable to find manufacturer.")
        return man


ASSET_CODE = AssetCodeParamType
ASSET_MANUFACTURER = AssetManufacturerParamType
