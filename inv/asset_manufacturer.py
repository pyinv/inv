"""Classes and schemas for Manufacturer."""
from pathlib import Path
from typing import TYPE_CHECKING, Any, List

from pydantic import BaseModel
from yaml import SafeLoader, load

if TYPE_CHECKING:
    from .inventory import Inventory
    from .asset_model import AssetModel  # noqa: F401


class AssetManufacturer(BaseModel):
    """A manufacturer of asset."""

    name: str
    path: Path

    @classmethod
    def load_from_file(
            cls,
            path: Path,
            inv: 'Inventory',
    ) -> 'AssetManufacturer':
        """Load a model from a path."""
        data_path = path.joinpath("data.yml")

        data: Any = load(data_path.open(mode='r'), Loader=SafeLoader)
        data.update({'path': path})
        return cls(**data)

    @classmethod
    def get_all(cls, inv: 'Inventory') -> List['AssetManufacturer']:
        """Get all manufacturers."""
        vals = []
        for entry in inv.meta_dir.iterdir():
            if entry.is_dir():
                man = AssetManufacturer.load_from_file(entry, inv)
                vals.append(man)
        return vals

    def get_models(self, inv: 'Inventory') -> List['AssetModel']:
        """Get all models from this manufacturer."""
        return inv.get_models_by_manufacturer(self)
