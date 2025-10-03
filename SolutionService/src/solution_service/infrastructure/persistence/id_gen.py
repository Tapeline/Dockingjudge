import uuid

from solution_service.application.interfaces.storage import IdGenerator


class DefaultUUIDGenerator(IdGenerator):
    def new_id(self) -> str:
        return str(uuid.uuid4())
