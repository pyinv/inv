"""Abstract Base Class for an Asset Code."""
from abc import ABCMeta, abstractmethod
from typing import ClassVar, List, Pattern


class AbstractAssetCode(metaclass=ABCMeta):
    """An abstract class defining functionality for an asset code."""

    name: ClassVar[str]
    format_regex: ClassVar[Pattern[str]]

    def generate(
        self,
        *,
        quantity: int = 1,
    ) -> List[str]:
        """Generate asset codes."""
        code_list: List[str] = []
        for _ in range(quantity):
            code_list.append(self._generate_code())

        if not all(self.verify(x) for x in code_list):
            raise InvalidAssetCodeGenerationException(
                "An invalid asset code was generated.",
            )

        return code_list

    @abstractmethod
    def _generate_code(self) -> str:
        """Generate an individual asset code."""
        raise NotImplementedError

    @abstractmethod
    def verify(self, candidate: str) -> bool:
        """Verify whether a string is a valid asset code."""
        raise NotImplementedError


class InvalidAssetCodeGenerationException(Exception):
    """A generated asset code was invalid."""

    pass
