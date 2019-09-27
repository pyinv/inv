"""A asset of items."""
from pathlib import Path
from re import compile
from typing import TYPE_CHECKING, List, Optional, Union

from .asset import Asset

if TYPE_CHECKING:
    from .inventory import Inventory


class AssetTree:
    """A tree of assets."""

    path: Path
    container: Asset

    def __init__(self, path: Path, inv: 'Inventory') -> None:
        if not path.is_dir():
            raise ValueError(
                f"{path} is not a directory, but attempted to create AssetTree.",
            )

        self.path = path
        self.inv = inv

        container_path = path.joinpath("data.yml")

        if container_path.exists():
            self.container = Asset.load_from_file(container_path, inv)

            if not self.container.model.container:
                raise ValueError(
                    f"{self.container.name} is a {self.container.model.name}."
                    f"It cannot be a container.",
                )

        else:
            raise ValueError(f"Container path does not exist: {container_path}")

    def __repr__(self) -> str:
        """Get a string representation of an asset tree."""
        return f"{self.__class__.__name__}" \
               f"(path={self.path.absolute()}, container={self.container})"

    @property  # Cache in future
    def contents(self) -> List[Union[Asset, 'AssetTree']]:
        """Get the contents of the container."""
        candidates = []
        for entry in self.path.iterdir():
            if entry.is_dir():
                candidates.append(entry)
            if entry.suffix == ".yml":
                candidates.append(entry)

        # Format regex is too specific
        format_regex = compile("^[data|[A-Z]{3}-[A-Z2-7]{3}-[A-Z2-7]{3}_")
        children = [x for x in candidates if format_regex.match(x.stem) is not None]

        contents: List[Union[Asset, 'AssetTree']] = []

        for child in children:
            if child.is_dir():
                contents.append(self.__class__(child, self.inv))
            else:
                contents.append(Asset.load_from_file(child, self.inv))
        return contents

    def find_asset_by_asset_code(
            self,
            org: str,
            asset_code: str,
    ) -> Optional[Union[Asset, 'AssetTree']]:
        """Find an asset or asset tree within this one by code."""
        # This can also certainly be done more efficiently.

        for entry in self.contents:
            if isinstance(entry, AssetTree):
                look = entry.container
            elif isinstance(entry, Asset):
                look = entry

            if look.asset_code == f"{org}-{asset_code[:3]}-{asset_code[3:]}":
                return entry

            if isinstance(entry, AssetTree):
                return entry.find_asset_by_asset_code(org, asset_code)
        return None
