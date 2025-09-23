from judgelet.application.interfaces import LanguageBackendRepository
from judgelet.domain.execution import LanguageBackend
from judgelet.domain.files import Solution
from judgelet.infrastructure.languages.lang_list import LANGUAGES


class LanguageBackendRepositoryImpl(LanguageBackendRepository):
    def create_backend(
            self, name: str, solution: Solution
    ) -> LanguageBackend | None:
        if name not in LANGUAGES:
            return None
        backend_cls = LANGUAGES[name]
        backend = backend_cls()
        return backend
