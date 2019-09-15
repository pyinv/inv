"""The main inventory class."""

from pathlib import Path
from typing import Type, TypeVar

from .asset_code import AbstractAssetCode

AssetCodeVar = TypeVar("AssetCodeVar", bound=AbstractAssetCode)


class Inventory:
    """An inventory, of assets, in locations."""

    def __init__(
        self,
        root: Path,
        *,
        asset_code_type: Type[AssetCodeVar],
        meta_dir: str = "meta",
    ):
        self.asset_code_type = asset_code_type
