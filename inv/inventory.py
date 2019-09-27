"""The main inventory class."""

from pathlib import Path
from typing import TYPE_CHECKING, Optional, Type, TypeVar, Union

from .asset import Asset
from .asset_tree import AssetTree

if TYPE_CHECKING:
    from .asset_code import AbstractAssetCode

AssetCodeVar = TypeVar("AssetCodeVar", bound='AbstractAssetCode')


class Inventory:
    """An inventory, of asset, in locations."""

    def __init__(
        self,
        root_path: Path,
        *,
        asset_code_type: Type[AssetCodeVar],
        org: str,
        meta_dir: str = "meta",
    ):
        self.asset_code_type = asset_code_type
        self.root_path = root_path
        self.org = org
        self.meta_dir = root_path.joinpath(meta_dir)

    @property
    def tree(self) -> AssetTree:
        """Get the asset tree at the root of the inventory."""
        return AssetTree(self.root_path)

    @property
    def asset_code(self) -> 'AbstractAssetCode':
        """Get the asset code class."""
        return self.asset_code_type.get_instance(self)

    def find_asset_by_code(self, asset_code: str) -> Optional[Union[AssetTree, Asset]]:
        """Find an asset or asset tree by code."""
        return self.tree.find_asset_by_asset_code(self.org, asset_code)
