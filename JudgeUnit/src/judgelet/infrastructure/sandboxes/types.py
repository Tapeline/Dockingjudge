from types import MappingProxyType

from typing import Final

from judgelet.application.interfaces import SandboxFactory
from judgelet.config import SandboxType
from judgelet.infrastructure.sandboxes.simple import (
    SimpleSandboxFactory
)
from judgelet.infrastructure.sandboxes.bubblewrap import (
    BubblewrapSandboxFactory
)

_SANDBOXES: Final = MappingProxyType({
    SandboxType.SIMPLE: SimpleSandboxFactory,
    SandboxType.BUBBLEWRAP: BubblewrapSandboxFactory,
})


def get_sandbox_factory(sandbox_type: SandboxType) -> SandboxFactory:
    """Retrieve a sandbox factory that corresponds to desired sandbox type."""
    try:
        return _SANDBOXES[sandbox_type]()
    except KeyError as exc:
        raise ValueError(f"Unregistered sandbox type {sandbox_type}") from exc
