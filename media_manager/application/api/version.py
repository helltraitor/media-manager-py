from dataclasses import dataclass
from typing import TypeAlias


Self: TypeAlias = "Version"


@dataclass(eq=True)
class Version:
    __major: int | None = None
    __minor: int | None = None
    __patch: int | None = None
    __other: str | None = None

    @property
    def major(self) -> int | None:
        return self.__major

    @property
    def minor(self) -> int | None:
        return self.__minor

    @property
    def patch(self) -> int | None:
        return self.__patch

    @property
    def other(self) -> str | None:
        return self.__other

    def exact(self, other: Self) -> bool:
        return all((lhs == rhs for lhs, rhs in zip(self.tuple(), other.tuple())))

    def tuple(self) -> tuple[int | None, int | None, int | None, str | None]:
        return self.__major, self.__minor, self.__patch, self.__other

    def match(self, other: Self) -> bool:
        for lhs, rhs in zip(self.tuple(), other.tuple()):
            if lhs is None or rhs is None:
                continue
            if lhs != rhs:
                return False
        return True
