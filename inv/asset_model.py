"""
Classes and schemas for Models.

A model is a specific variety of an asset, but is not a specific instance of
that asset.
"""
from pathlib import Path
from re import sub
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel
from yaml import SafeLoader, load

from .asset_manufacturer import AssetManufacturer

if TYPE_CHECKING:
    from .inventory import Inventory


class AssetModel(BaseModel):
    """A model of asset."""

    name: str
    container: bool
    path: Path

    manufacturer: AssetManufacturer

    @classmethod
    def load_from_file(cls, path: Path, inv: 'Inventory') -> 'AssetModel':
        """Load a model from a yml file."""
        data: Any = load(path.open(mode='r'), Loader=SafeLoader)

        manufacturer = AssetManufacturer.load_from_file(path.parent, inv)

        data.update({'manufacturer': manufacturer})
        data.update({'path': path})

        model = cls(**data)

        if path.stem == model.calculate_filename():
            return model

        raise ValueError(
            f"Bad filename for model: {path.name}. "
            f"Expected {model.calculate_filename()}{path.suffix}",
        )

    def calculate_filename(self) -> str:
        """Calculate the filename from the data."""
        name_format = self.name.lower().replace(" ", "_").replace("-", "_")
        name_format = sub('[^a-z0-9_]+', '', name_format)
        return name_format
