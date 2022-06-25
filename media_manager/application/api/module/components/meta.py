import logging

from media_manager.application import utils
from media_manager.application.api.context import Context

from .abc import Component


class CMetaInformation(Component):
    def __init__(self, context: Context):
        super().__init__(context)
        self.__id = context.checked("id", str)
        self.__name = context.checked("name", str) or "Unknown"
        self.__version = context.checked("version", str)

    def id(self) -> str:
        if self.__id is None:
            logging.error("%s: Attempting to return None id instead of string", utils.name(self))
            raise RuntimeError("Id must be provided in context or this method must be overrided")
        return self.__id

    def name(self) -> str:
        return self.__name

    def version(self) -> str:
        if self.__version is None:
            logging.error("%s: Attempting to return None version instead of string", utils.name(self))
            raise RuntimeError("Version must be provided in context or this method must be overrided")
        return self.__version
