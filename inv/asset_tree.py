"""A asset of items."""
from pathlib import Path
from re import compile
from typing import List, Optional, Union

from .asset import Asset


class AssetTree:
    """A tree of assets."""

    path: Path
    container: Optional[Asset] = None

    def __init__(self, path: Path) -> None:
        if not path.is_dir():
            raise ValueError(
                f"{path} is not a directory, but attempted to create AssetTree.",
            )

        self.path = path

        container_path = path.joinpath("data.yml")

        if container_path.exists():
            self.container = Asset.load_from_file(container_path)

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
                contents.append(self.__class__(child))
            else:
                contents.append(Asset.load_from_file(child))
        return contents
