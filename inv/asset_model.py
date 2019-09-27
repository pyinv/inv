"""
Classes and schemas for Models.

A model is a specific variety of an asset, but is not a specific instance of
that asset.
"""
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from yaml import SafeLoader, load


class AssetModel(BaseModel):
    """A model of asset."""

    name: str
    container: bool

    # TODO: Manufacturer

    @classmethod
    def load_from_file(cls, path: Path, inv: 'Inventory') -> 'AssetModel':
        """Load a model from a yml file."""
        data: Any = load(path.open(mode='r'), Loader=SafeLoader)

        # TODO: Check filename

        return cls(**data)
