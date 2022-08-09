import logging

from media_manager.application.api.module import PrimitiveModule
from media_manager.application.api.module.components import CShutdown
from media_manager.application.api.module.features import FShutdown


class Keeper:
    def __init__(self):
        self.__modules: dict[str, PrimitiveModule] = {}

    def append(self, module: PrimitiveModule):
        if module.meta().id() in self.__modules:
            _double_add_warning(type(self).__name__, self.__modules[module.meta().id()], module)
            return
        self.__modules[module.meta().id()] = module

    def drop(self):
        for module in self.__modules.values():
            component = module.components().get(FShutdown, CShutdown)
            if component is not None:
                component.shutdown()

    def contains(self, *, id: str | None = None, module: PrimitiveModule | None = None) -> bool:
        if id is not None:
            return id in self.__modules
        if module is not None:
            return module.meta().id() in self.__modules
        raise ValueError("One of kwargs must be used: id or module")

    def list(self) -> list[PrimitiveModule]:
        return list(self.__modules.values())

    def remove(self, *, id: str | None = None, module: PrimitiveModule | None = None):
        id = id or (module is not None and module.meta().id()) or None
        if id is not None:
            if self.__modules.pop(id, None) is None:
                logging.error("%s: Attempting to remove non-existing module with id `%s`",
                              type(self).__name__, id)
            return
        raise ValueError("One of kwargs must be used: id or module")


# Function was part of add method but was moved out for reducing cognitive load
def _double_add_warning(cls: str, existed: PrimitiveModule, new: PrimitiveModule):
    logging.warning("%s: Attempting to override already loaded module with id `%s`",
                    cls, existed.meta().id(),
                    extra={
                        "existed_name": existed.meta().name(),
                        "existed_version": existed.meta().version(),
                        "new_name": new.meta().name(),
                        "new_version": new.meta().id()})
