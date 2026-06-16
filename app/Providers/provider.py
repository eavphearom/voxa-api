from app.Providers.container import Container
from app.config.binding.repositories import REPOSITORY_BINDINGS
from app.config.binding.services import SERVICE_BINDINGS


def register_application_bindings(container: Container) -> None:
    for contract, binding in REPOSITORY_BINDINGS.items():
        if isinstance(binding, type):
            container.register(contract, lambda binding=binding: binding())
        else:
            container.register(contract, lambda binding=binding: binding(container))

    for contract, factory in SERVICE_BINDINGS.items():
        container.register(contract, lambda factory=factory: factory(container))
