import uuid
from typing import override

from solution_service.application.interfaces.storage import IdGenerator


class DefaultUUIDGenerator(IdGenerator):
    @override
    def new_id(self) -> str:
        return str(uuid.uuid4())
