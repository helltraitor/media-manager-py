import logging

from .module import Module


class ModulesKeeper:
    def __init__(self):
        self.__modules: dict[str, Module] = {}

    def module_add(self, module: Module):
        if module.id in self.__modules:
            _double_module_add_warning(type(self).__name__, self.__modules[module.id], module)
            return
        self.__modules[module.id] = module

    def module_remove(self, module_id: str):
        module = self.modules.pop(module_id)
        module = self.__modules.pop(module_id)

    def module_all(self) -> list[Module]:
        return list(self.__modules.values())


# Separated warning function to reduce cognitive load
def _double_module_add_warning(cls_name: str, old: Module, new: Module):
    old_module_meta = {
        "meta": old.module_meta,
        "name": old.module_meta.name() if old.module_meta is not None else "Error",
        "version": old.module_meta.version() if old.module_meta is not None else "Error",
    }
    new_module_meta = {
        "meta": new.module_meta,
        "name": new.module_meta.name() if new.module_meta is not None else "Error",
        "version": new.module_meta.version() if new.module_meta is not None else "Error",
    }
    logging.warning(f"{cls_name}: Attempting to override already loaded module with id `{old.id}`", extra={
        "new_module_meta": new_module_meta,
        "old_module_meta": old_module_meta,
    })
