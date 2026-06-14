from app.Providers.container import Container, container
from app.Providers.provider import register_application_bindings

register_application_bindings(container)

__all__ = ["Container", "container", "register_application_bindings"]
