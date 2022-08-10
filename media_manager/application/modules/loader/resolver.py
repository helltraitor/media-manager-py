from collections.abc import Sequence, Generator, Iterable
from dataclasses import dataclass

from media_manager.application.api.module import ModuleLoader
from media_manager.application.api.version import Version


class StillUsingError(Exception):
    pass


@dataclass
class ResolverNode:
    loader: ModuleLoader
    depends: list[tuple[str, Version]]


class Resolver:
    def __init__(self, loaders: Sequence[ModuleLoader] | None = None) -> None:
        self.__pended = [ResolverNode(loader, [*loader.dependencies()]) for loader in (loaders or ())]
        self.__loaded: list[ResolverNode] = []
        self.__satisfied: list[tuple[str, Version]] = []

    def append(self, loader: ModuleLoader) -> None:
        self.__pended.append(ResolverNode(loader, [*loader.dependencies()]))

    def extend(self, loaders: Iterable[ModuleLoader]):
        self.__pended.extend((ResolverNode(loader, [*loader.dependencies()]) for loader in loaders))

    def depended(self, loader: ModuleLoader) -> list[ModuleLoader]:
        dependency = loader.name(), loader.version()
        return [node.loader for node in self.__loaded if dependency in node.depends]

    def pended(self) -> list[ModuleLoader]:
        return [node.loader for node in self.__pended]

    def remove(self, loader: ModuleLoader) -> None:
        dependency = loader.name(), loader.version()
        for node in self.__loaded:
            if dependency in node.depends:
                raise StillUsingError(f"Unable to remove module {loader} while it still using by {node.loader}")

        # TODO: Check node == other node
        self.__loaded.remove(ResolverNode(loader, [*loader.dependencies()]))

    def resolve(self) -> Generator[list[ModuleLoader], None, None]:
        while self.__pended:
            print("PENDED", self.__pended)
            resolved: list[ResolverNode] = []
            for node in self.__pended:
                # Probably more efficient way to match versions exits
                #   but for now is unnecessary
                for dependency in node.depends:
                    unmatched = True
                    for satisfied in self.__satisfied:
                        if dependency[0] == satisfied[0] and dependency[1].match(satisfied[1]):
                            unmatched = False
                            break
                    if unmatched and node.depends:
                        break
                else:
                    resolved.append(node)

            # Cannot load any module
            if not resolved:
                return

            for node in resolved:
                dependency = node.loader.name(), node.loader.version()
                self.__satisfied.append(dependency)
                self.__pended.remove(node)

            yield [node.loader for node in resolved]

    def satisfied(self) -> frozenset[tuple[str, Version]]:
        return frozenset(self.__satisfied)
