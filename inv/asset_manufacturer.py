"""Classes and schemas for Manufacturer."""
from pathlib import Path
from re import sub
from typing import TYPE_CHECKING, Any, List

from pydantic import BaseModel
from yaml import SafeDumper, SafeLoader, dump, load

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

    @classmethod
    def create_instance(cls, inv: 'Inventory', name: str) -> 'AssetManufacturer':
        """Create a new instance."""
        name_format = name.lower().replace(" ", "_").replace("-", "_")
        name_format = sub('[^a-z0-9_]+', '', name_format)

        path = inv.meta_dir.joinpath(name_format)

        return cls(
            name=name,
            path=path,
        )

    def calculate_filename(self) -> str:
        """Calculate the filename from the data."""
        name_format = self.name.lower().replace(" ", "_").replace("-", "_")
        name_format = sub('[^a-z0-9_]+', '', name_format)
        return name_format

    def get_models(self, inv: 'Inventory') -> List['AssetModel']:
        """Get all models from this manufacturer."""
        return inv.get_models_by_manufacturer(self)

    def save(self, inv: 'Inventory', overwrite: bool = False) -> None:
        """Save to a file."""
        if self.path.exists():
            if not overwrite:
                raise FileExistsError("Manufacturer already exists.")
        else:
            self.path.mkdir()

        file_path = self.path.joinpath("data.yml")

        data = {
            'name': self.name,
        }

        dump(data, file_path.open("w"), SafeDumper)
