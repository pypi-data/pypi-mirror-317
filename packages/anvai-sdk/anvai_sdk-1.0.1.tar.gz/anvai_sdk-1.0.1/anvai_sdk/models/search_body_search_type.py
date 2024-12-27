from enum import Enum


class SearchBodySearchType(str, Enum):
    CGS = "CGS"
    CS = "CS"

    def __str__(self) -> str:
        return str(self.value)
