from .abc import Component


class CMetaInformation(Component):
    def id(self) -> str:
        raise NotImplementedError("This method must be implemented in subclass")

    def name(self) -> str:
        raise NotImplementedError("This method must be implemented in subclass")

    def version(self) -> str:
        raise NotImplementedError("This method must be implemented in subclass")
