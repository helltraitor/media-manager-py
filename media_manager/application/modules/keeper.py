import logging

from media_manager.application.api.module import Module


class ModulesKeeper:
    def __init__(self):
        self.__modules: dict[str, Module] = {}

    def module_add(self, module: Module):
        if module.id in self.__modules:
            _double_module_add_warning(type(self).__name__, self.__modules[module.id], module)
            return
        self.__modules[module.id] = module

    def module_list(self) -> list[Module]:
        return list(self.__modules.values())

    def module_remove(self, module_id: str):
        module = self.__modules.pop(module_id, None)
        if module is None:
            logging.error(f'{type(self).__name__}: Attempting to remove non-existing module with `{module_id}` id')


# Separated warning function to reduce cognitive load
def _double_module_add_warning(cls_name: str, old: Module, new: Module):
    old_module_meta = {
        "meta": old.meta,
        "name": old.meta.name() if old.meta is not None else "Error",
        "version": old.meta.version() if old.meta is not None else "Error",
    }
    new_module_meta = {
        "meta": new.meta,
        "name": new.meta.name() if new.meta is not None else "Error",
        "version": new.meta.version() if new.meta is not None else "Error",
    }
    logging.warning(f"{cls_name}: Attempting to override already loaded module with id `{old.id}`", extra={
        "new_module_meta": new_module_meta,
        "old_module_meta": old_module_meta,
    })
