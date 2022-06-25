from typing import TypeAlias

from .result import Result


Content: TypeAlias = dict[str, str]


class Reply:
    def __init__(self, result: Result, *, content: Content | None = None):
        self.__content = content or {}
        self.__result = result

    def content(self) -> Content:
        return self.__content

    def result(self) -> Result:
        return self.__result
