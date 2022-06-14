class Reply:
    def __init__(self, content: dict[str, str]):
        self.__content = content

    def content(self) -> dict[str, str]:
        return self.__content
