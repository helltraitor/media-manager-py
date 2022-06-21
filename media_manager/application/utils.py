import logging

from typing import Any, Type, TypeVar

T = TypeVar("T")


def name(entity: Any) -> str:
    if hasattr(entity, "__name__"):
        return entity.__name__
    if hasattr(entity, "__class__") and hasattr(entity.__class__, "__name__"):
        return entity.__class__.__name__
    logging.error("%s: Entity %s has no name", name.__name__, repr(entity))
    raise RuntimeError(f"Entity {entity} has no name")


def critical_cast(inst: Any, guard: Type[T]) -> T:
    if isinstance(inst, guard):
        return inst
    logging.error("%s: %s is not instance of %s", name(critical_cast), name(inst), name(guard))
    raise RuntimeError(f"{name(inst)} is not instance of {name(guard)}")


def dynamic_cast(inst: Any, guard: Type[T]) -> T | None:
    if isinstance(inst, guard):
        return inst
    return None
