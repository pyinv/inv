"""Classes and schemas for Manufacturer."""
from pydantic import BaseModel


class AssetManufacturer(BaseModel):
    """A manufacturer of asset."""

    name: str
