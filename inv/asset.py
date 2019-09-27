"""Classes and schemas for an asset."""
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel
from yaml import SafeLoader, load

from inv.asset_model import AssetModel

if TYPE_CHECKING:
    from inv.inventory import Inventory


class Asset(BaseModel):
    """An asset."""

    path: Path
    asset_code: str
    asset_model: str
    name: str

    @classmethod
    def load_from_file(cls, path: Path, inv: 'Inventory') -> 'Asset':
        """Load an asset from a yml file."""
        data: Any = load(path.open(mode='r'), Loader=SafeLoader)

        # Check that the code and name in the filename match.

        # Check that the model exists

        return cls(**{
            **data,
            'path': path,
        })

    @property
    def model(self) -> AssetModel:
        """The model of this asset."""
        pass

    # @property
    # def container(self) -> AssetTree:
    #     """The container that this asset is within."""

    def display(self) -> None:
        """Print the information."""
        print(f"Asset Code: {self.asset_code}")
        # print(f"Location: {self.container.container.name}")
        print(f"Model: {self.asset_model}")
        print(f"Name: {self.name}")
