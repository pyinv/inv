"""Classes and schemas for an asset."""
from pathlib import Path
from re import sub
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel
from yaml import SafeDumper, SafeLoader, dump, load

from .asset_model import AssetModel

if TYPE_CHECKING:
    from .asset_tree import AssetTree
    from .inventory import Inventory


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

        model = inv.get_model(data["asset_model"])

        data.update({'path': path})
        data.update({'model': model})

        asset = cls(**data)

        if model.container and path.name != "data.yml":
            raise ValueError(
                f"Asset Model {model.name} must "
                f"be stored as a container",
            )

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

    def display(self, inv: 'Inventory') -> None:
        """Print the information."""
        print(f"Asset Code: {self.asset_code}")
        if self.path.stem == "data":
            # Container
            print(f"Current Location: {self.path.parents[1].stem}")
        else:
            print(f"Current Location: {self.path.parent.stem}")

        print(f"Model: {self.model.name}")
        print(f"Name: {self.name}")

    def calculate_filename(self) -> str:
        """Calculate the stem of the filename."""
        name_format = self.name.lower().replace(" ", "_").replace("-", "_")
        name_format = sub('[^a-z0-9_]+', '', name_format)
        return f"{self.asset_code}_{self.model.calculate_filename()}_{name_format}"

    @classmethod
    def save_new(
        cls,
        code: str,
        model: AssetModel,
        name: str,
        location: 'AssetTree',
        inv: 'Inventory',
    ) -> None:
        """Save an new instance of asset."""
        human_code = inv.asset_code.human_format(code)

        name_format = name.lower().replace(" ", "_").replace("-", "_")
        name_format = sub('[^a-z0-9_]+', '', name_format)
        file_stem = f"{human_code}_" \
                    f"{model.calculate_filename()}_" \
                    f"{name_format}"

        if model.container:
            folder = location.path.joinpath(file_stem)
            folder.mkdir()
            path = folder.joinpath("data.yml")
        else:
            path = location.path.joinpath(f"{file_stem}.yml")

        if path.exists():
            raise ValueError("This asset already exists.")

        data = {
            'asset_code': human_code,
            'asset_model': model.namespaced_name,
            'name': name,
        }

        dump(data, path.open("w"), SafeDumper)
