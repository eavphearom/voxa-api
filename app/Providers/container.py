from collections.abc import Callable
from typing import Any, TypeVar


DependencyT = TypeVar("DependencyT")


class Container:
    def __init__(self) -> None:
        self._factories: dict[type[Any], Callable[[], Any]] = {}

    def register(
        self,
        contract: type[DependencyT],
        factory: Callable[[], DependencyT],
    ) -> None:
        self._factories[contract] = factory

    def resolve(self, contract: type[DependencyT]) -> DependencyT:
        factory = self._factories.get(contract)
        if factory is None:
            raise LookupError(f"No dependency registered for {contract.__name__}")
        return factory()


container = Container()
