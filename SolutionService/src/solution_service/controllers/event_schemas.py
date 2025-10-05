from pydantic import BaseModel

from solution_service.controllers.schemas import GroupProtocolSchema
from solution_service.domain.abstract import TaskType


class MQSolutionAnswer(BaseModel):
    id: str
    score: int
    detailed_verdict: str
    short_verdict: str
    group_scores: dict[str, int]
    protocol: dict[str, GroupProtocolSchema]
    compilation_error: str | None = None


class MQUserEventTarget(BaseModel):
    id: int


class MQUserEvent(BaseModel):
    event: str
    object: MQUserEventTarget


class MQContestEventTargetPage(BaseModel):
    id: int
    type: TaskType


class MQContestEventTarget(BaseModel):
    id: int
    pages: list[MQContestEventTargetPage]


class MQContestEvent(BaseModel):
    event: str
    object: MQContestEventTarget


class MQTaskEventTarget(BaseModel):
    id: int


class MQTaskEvent(BaseModel):
    event: str
    object: MQUserEventTarget
