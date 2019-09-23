"""A asset of items."""
from re import compile
from pathlib import Path
from typing import Optional, Set

from .asset import Asset


class AssetTree:

    path: Path
    container: Optional[Asset] = None
    

    def __init__(self, path: Path) -> None:
        self.path = path

        if path.joinpath("data.yml").exists():
            print()


    @classmethod
    def find_from_dir(cls, path: Path) -> 'AssetTree':
        """Create an asset tree from a directory."""
        if not path.is_dir():
            raise ValueError(
                f"{path} is not a directory, but attempted to list files."
            )

        candidates = []
        for entry in path.iterdir():
            if path.is_dir():
                candidates.append(entry)
            if entry.suffix == "yml":
                candidates.append(entry)

        format_regex = compile("^[data|[A-Z]{3}-[A-Z2-7]{3}-[A-Z2-7]{3}_")  # Oops too specific
        children = [x for x in candidates if format_regex.match(x.stem) is not None]
        return cls(Path(""))

    def __str__(self) -> str:
        """Get a string representation of an asset tree."""
        return f"{self.__class__.__name__}(path={self.path.absolute()}, container={self.container})"
