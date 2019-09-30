"""The main inventory class."""

from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Type, TypeVar, Union

from .asset import Asset
from .asset_manufacturer import AssetManufacturer
from .asset_model import AssetModel
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
        return AssetTree(self.root_path, self)

    @property
    def asset_code(self) -> 'AbstractAssetCode':
        """Get the asset code class."""
        return self.asset_code_type.get_instance(self)

    def find_asset_by_code(self, asset_code: str) -> Optional[Union[AssetTree, Asset]]:
        """Find an asset or asset tree by code."""
        return self.tree.find_asset_by_asset_code(self.org, asset_code)

    def get_manufacturer(self, formatted_name: str) -> AssetManufacturer:
        """Find a manufacturer."""
        try:
            path = self.meta_dir.joinpath(formatted_name)
            return AssetManufacturer.load_from_file(path, self)
        except FileNotFoundError:
            raise ValueError("No such manufacturer.")

    def get_model(self, formatted_name: str) -> AssetModel:
        """Find a model."""
        path = self.meta_dir.joinpath(f"{formatted_name}.yml")

        if not path.exists():
            raise FileNotFoundError(f"Unable to find {formatted_name}")
        else:
            return AssetModel.load_from_file(path, self)

    def get_models_by_manufacturer(self, man: AssetManufacturer) -> List[AssetModel]:
        """Get all models from a manufacturer."""
        models = []
        for model_file in man.path.iterdir():
            if model_file.stem != "data":  # Ignore manufacturer file
                models.append(AssetModel.load_from_file(model_file, self))
        return models
