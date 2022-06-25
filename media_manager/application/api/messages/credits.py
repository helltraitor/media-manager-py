class Credits:
    def __init__(self, name: str, version: str, id: str, **details: str):
        self.__details = details
        self.__name = name
        self.__version = version
        self.__id = id

    def __repr__(self):
        return f'Credits("{self.__name}", "{self.__version}", "{self.__id}")'

    def copy(self) -> "Credits":
        return Credits(self.__name, self.__version, self.__id, **self.__details.copy())

    def details(self) -> dict[str, str]:
        return self.__details.copy()

    def id(self) -> str:
        return self.__id

    def name(self) -> str:
        return self.__name

    def version(self) -> str:
        return self.__version
