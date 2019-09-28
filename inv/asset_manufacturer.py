"""Classes and schemas for Manufacturer."""
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from yaml import load, SafeLoader


class AssetManufacturer(BaseModel):
    """A manufacturer of asset."""

    name: str

    @classmethod
    def load_from_file(cls, path: Path, inv: 'Inventory') -> 'AssetManufacturer':
        """Load a model from a path."""
        data_path = path.joinpath("data.yml")

        data: Any = load(data_path.open(mode='r'), Loader=SafeLoader)

        return cls(**data)
