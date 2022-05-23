import logging

from .module import Module


class ModulesKeeper:
    def __init__(self):
        self.modules: dict[str, Module] = {}

    def module_add(self, module: Module):
        if module.id in self.modules:
            return
        self.modules[module.id] = module

    def module_remove(self, module_id: str):
        module = self.modules.pop(module_id)
