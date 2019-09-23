"""The main inventory class."""

from pathlib import Path
from typing import Type, TypeVar

from .asset_code import AbstractAssetCode
from .asset_tree import AssetTree

AssetCodeVar = TypeVar("AssetCodeVar", bound=AbstractAssetCode)


class Inventory:
    """An inventory, of asset, in locations."""

    def __init__(
        self,
        root_path: Path,
        *,
        asset_code_type: Type[AssetCodeVar],
        meta_dir: str = "meta",
    ):
        self.asset_code_type = asset_code_type
        self.root_path = root_path
        self.meta_dir = root_path.joinpath(meta_dir)

    @property
    def tree(self) -> AssetTree:
        """Get the asset tree at the root of the inventory."""
        return AssetTree(self.root_path)
