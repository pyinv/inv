"""Classes and schemas for an asset."""
from pathlib import Path

from pydantic import BaseModel


class Asset(BaseModel):
    """An asset."""

    asset_code: str
    asset_model: str
    name: str

    def load_from_file(path: Path):
        """Load an asset from a yml file."""
        pass