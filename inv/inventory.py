"""The main inventory class."""

from pathlib import Path
from typing import Optional, Type, TypeVar, Union

from .asset import Asset
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

    def find_asset_by_code(self, asset_code: str) -> Optional[Union[AssetTree, Asset]]:
        """Find an asset or asset tree by code."""
        return self.tree.find_asset_by_asset_code(asset_code)
