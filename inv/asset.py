"""Classes and schemas for an asset."""
from pathlib import Path
from re import sub
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

    model: AssetModel

    @classmethod
    def load_from_file(
            cls,
            path: Path,
            inv: 'Inventory',
            *,
            ignore_filename: bool = False,
    ) -> 'Asset':
        """Load an asset from a yml file."""
        data: Any = load(path.open(mode='r'), Loader=SafeLoader)

        model = AssetModel.load_from_file(
            inv.meta_dir.joinpath(Path(data["asset_model"] + ".yml")),
            inv,
        )

        data.update({'path': path})
        data.update({'model': model})

        asset = cls(**data)

        if ignore_filename:
            return asset

        # Check the filename
        expected_name = asset.calculate_filename()
        if path.stem == expected_name:
            return asset

        if path.name == "data.yml":
            if path.parent.name == expected_name:
                return asset
            if path.parent == Path("."):
                # Root
                return asset

        raise ValueError(f"Bad filename: {path}. Expected: {expected_name}.yml")

    def display(self) -> None:
        """Print the information."""
        print(f"Asset Code: {self.asset_code}")
        # print(f"Location: {self.parent.container.name}")
        print(f"Model: {self.asset_model}")
        print(f"Name: {self.name}")

    def calculate_filename(self) -> str:
        """Calculate the stem of the filename."""
        name_format = self.name.lower().replace(" ", "_").replace("-", "_")
        name_format = sub('[^a-z0-9_]+', '', name_format)
        return f"{self.asset_code}_{self.model.calculate_filename()}_{name_format}"
