from media_manager.application.api.context import Context
from media_manager.application.api.module.components import CDefaultWidget
from media_manager.application.api.module.features import FDefaultWidget


class CCloneDefaultWidget(CDefaultWidget):
    def __init__(self, context: Context):
        self.__context = context

        # Todo: Make deferred initialization of default widget without using defer feature
        # We need to put super call down because in opposite case
        #     CDefaultWidget will try to use title before context will set up
        super().__init__(context)

    def title(self) -> str:
        return f"Clone #{self.__context.unwrap('id', str)}"
