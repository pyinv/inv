"""The main inventory class."""

from typing import Type, TypeVar

from .asset_code import AbstractAssetCode

AssetCodeVar = TypeVar("AssetCodeVar", bound=AbstractAssetCode)


class Inventory:
    """An inventory, of assets, in locations."""

    def __init__(
        self,
        *,
        asset_code_type: Type[AssetCodeVar],
    ):
        self.asset_code_type = asset_code_type
