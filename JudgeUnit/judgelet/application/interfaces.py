from abc import ABC, abstractmethod
from typing import Mapping

from judgelet.domain.execution import LanguageBackend
from judgelet.domain.files import FileSystem, Solution
from judgelet.domain.sandbox import Sandbox


class LanguageBackendRepository(ABC):
    @abstractmethod
    def create_backend(
            self, name: str, solution: Solution
    ) -> LanguageBackend | None:
        """Create backend or return None if none found by name."""
        raise NotImplementedError


class SandboxFactory(ABC):
    @abstractmethod
    def __call__(
            self,
            fs: FileSystem,
            sandbox_dir: str,
            encoding: str | None = None,
            environment: Mapping[str, str] | None = None
    ) -> Sandbox:
        """Create sandbox."""
        raise NotImplementedError
