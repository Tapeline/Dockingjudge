from typing import override

from judgelet.application.interfaces import LanguageBackendFactory
from judgelet.domain.execution import LanguageBackend
from judgelet.domain.files import Solution
from judgelet.infrastructure.languages.lang_list import LANGUAGES


class DefaultLanguageBackendFactory(LanguageBackendFactory):
    """Default implementation for language backend factory."""

    @override
    def create_backend(
        self, name: str, solution: Solution,
    ) -> LanguageBackend | None:
        if name not in LANGUAGES:
            return None
        backend_cls = LANGUAGES[name]
        return backend_cls()  # type: ignore[misc]
