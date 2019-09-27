"""Classes and schemas for an asset."""
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from yaml import SafeLoader, load


class Asset(BaseModel):
    """An asset."""

    asset_code: str
    asset_model: str
    name: str

    @classmethod
    def load_from_file(cls, path: Path) -> 'Asset':
        """Load an asset from a yml file."""
        data: Any = load(path.open(mode='r'), Loader=SafeLoader)
        return cls(**data)

    def display(self) -> None:
        """Print the information."""
        print(f"Asset Code: {self.asset_code}")
        print(f"Asset Model: {self.asset_model}")
        print(f"Asset Name: {self.name}")
