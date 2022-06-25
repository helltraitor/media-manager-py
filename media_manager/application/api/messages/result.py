import dataclasses
import logging

from media_manager.application import utils


@dataclasses.dataclass
class Result:
    status: str
    reason: str = ""

    def __post_init__(self):
        ALLOWED_STATUSES = (
            "OK", "ERROR"
        )

        if self.status not in ALLOWED_STATUSES:
            logging.error("%s: Attempting to use non-allowed status %s",
                          utils.name(self), self.status)
            raise RuntimeError(f"{self.status} is not allowed")

    def is_error(self) -> bool:
        return self.status == "ERROR"

    def is_ok(self) -> bool:
        return self.status == "OK"
