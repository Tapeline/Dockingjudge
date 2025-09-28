from types import MappingProxyType

from judgelet.domain.results import ExitState
from judgelet.domain.sandbox import SandboxExitCause

_CAUSE_TO_STATE = MappingProxyType({
    0: ExitState.FINISHED,
    SandboxExitCause.PROCESS_EXITED: ExitState.FINISHED,
    SandboxExitCause.TIME_LIMIT_EXCEEDED: ExitState.TIME_LIMIT,
    SandboxExitCause.MEMORY_LIMIT_EXCEEDED: ExitState.MEM_LIMIT,
})


def map_sandbox_cause_to_exit_state(cause: SandboxExitCause) -> ExitState:
    """Get exit state cause."""
    return _CAUSE_TO_STATE.get(cause, ExitState.ERROR)
