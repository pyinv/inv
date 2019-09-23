"""
Classes and schemas for Models.

A model is a specific variety of an asset, but is not a specific instance of
that asset.
"""
from pydantic import BaseModel


class AssetModel(BaseModel):
    """A model of asset."""

    name: str
    container: bool
