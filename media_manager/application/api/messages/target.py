from .credits import Credits


class Target:
    def __init__(self, name: str, version: str | None = None, **details: str):
        self.__name = name
        self.__version = version
        self.__details = details

    def name(self) -> str:
        return self.__name

    def details(self) -> dict[str, str]:
        return self.__details

    def match(self, credits: Credits) -> bool:
        if self.__version is not None:
            raise NotImplementedError("Target version matching is not implemented")
        lhs = self.details()
        rhs = credits.details()
        return self.__name == credits.name() and all(
            lhs[topic] == rhs[topic] for topic in lhs.keys() & rhs.keys())
