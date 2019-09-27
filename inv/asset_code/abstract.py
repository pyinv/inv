"""Abstract Base Class for an Asset Code."""
from abc import ABCMeta, abstractmethod
from re import compile
from typing import ClassVar, List

from inv import Inventory


class AbstractAssetCode(metaclass=ABCMeta):
    """An abstract class defining functionality for an asset code."""

    name: ClassVar[str]
    format_regex: ClassVar[str]

    def generate(
        self,
        *,
        quantity: int = 1,
    ) -> List[str]:
        """
        Generate validated asset codes.

        :param quantity: Number of codes to generate
        :return: A list of generated asset codes.
        """
        code_list: List[str] = []
        for _ in range(quantity):
            code_list.append(self._generate_code())

        if not all(self.verify(x) for x in code_list):
            raise InvalidAssetCodeGenerationException(
                "An invalid asset code was generated.",
            )

        return code_list

    def verify(self, candidate: str) -> bool:
        """
        Verify a candidate asset code.

        This function will check both the format and parity.

        :param candidate: An unformatted asset code.
        :return: True if valid code, false otherwise.
        """
        pattern = compile(self.format_regex)
        match = pattern.match(candidate)
        if match is None:
            return False
        return self._verify_code(candidate)

    def human_format(self, code: str) -> str:
        """Present the code in a human readable way."""
        return code

    @classmethod
    def get_instance(cls, inventory: Inventory) -> 'AbstractAssetCode':
        """Get an instance of this class."""
        return cls()

    @abstractmethod
    def _generate_code(self) -> str:
        """
        Generate an individual asset code.

        :return: An unformatted asset code.
        """
        raise NotImplementedError

    @abstractmethod
    def _verify_code(self, candidate: str) -> bool:
        """
        Verify whether a string is a valid asset code.

        :param candidate: An unformatted asset code.
        :return: True if valid code.
        """
        raise NotImplementedError


class InvalidAssetCodeGenerationException(Exception):
    """A generated asset code was invalid."""

    pass
