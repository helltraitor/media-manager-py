from typing import Protocol

from .credits import Credits
from .message import SignedMessage
from .reply import Reply


class MessageHandler(Protocol):
    def accepts(self, credits: Credits) -> bool: ...

    def process(self, message: SignedMessage) -> Reply: ...
