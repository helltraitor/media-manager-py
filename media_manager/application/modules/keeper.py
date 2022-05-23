import logging

from .module import Module


class ModulesKeeper:
    def __init__(self):
        self.__modules: dict[str, Module] = {}

    def module_add(self, module: Module):
        if module.id in self.__modules:
            return
        self.__modules[module.id] = module

    def module_remove(self, module_id: str):
        module = self.modules.pop(module_id)
        module = self.__modules.pop(module_id)

    def module_all(self) -> list[Module]:
        return list(self.__modules.values())
