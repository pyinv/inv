"""Custom Click ParamTypes."""
import re
from typing import Optional

import click

from inv.asset_manufacturer import AssetManufacturer
from inv.asset_model import AssetModel
from inv.asset_tree import AssetTree
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


class AssetModelParamType(click.ParamType):
    """ParamType for Model."""

    name = "model"

    def convert(
            self,
            value: str,
            _: Optional[click.Parameter],
            ctx: Optional[click.Context],
    ) -> AssetModel:
        """Convert."""
        inv = get_inv()

        name_format = value.lower().replace(" ", "_").replace("-", "_")
        name_format = re.sub('[^a-z0-9_/]+', '', name_format)

        REGEX = "^[a-z0-9_]+/[a-z0-9_]+$"

        if re.match(REGEX, name_format) is None:
            self.fail("Model must be namespaced in format manufacturer/model")

        try:
            model = inv.get_model(name_format)
        except FileNotFoundError:
            self.fail("Unable to find that model.")

        return model


class AssetTreeParamType(click.ParamType):
    """ParamType for AssetTree."""

    name = "asset_tree"

    def convert(
            self,
            value: str,
            _: Optional[click.Parameter],
            ctx: Optional[click.Context],
    ) -> Optional[AssetTree]:
        """Convert."""
        inv = get_inv()

        # Check the format, and convert to internal if needed.
        FULL_REGEX = f"^{inv.org}-([A-Z2-7]{{3}})-([A-Z2-7]{{3}})$"

        match = re.match(FULL_REGEX, value)

        if match is None:
            self.fail("asset code in wrong format")
            return None
        else:
            internal_value = match.group(1) + match.group(2)

            if not inv.asset_code.verify(internal_value):
                self.fail(f"failed to verify asset code: {internal_value}")

            asset = inv.find_asset_by_code(internal_value)

            if asset is None:
                self.fail(f"Unable to find container {value}")
            else:
                if not isinstance(asset, AssetTree):
                    self.fail(f"{value} is not a container")
                else:
                    return asset
        return None


ASSET_CODE = AssetCodeParamType
ASSET_MANUFACTURER = AssetManufacturerParamType
ASSET_MODEL = AssetModelParamType
ASSET_TREE = AssetTreeParamType
