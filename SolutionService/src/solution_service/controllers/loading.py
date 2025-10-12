from litestar.exceptions import ValidationException


def load_composite_task_id(composite_id: str) -> tuple[str, int]:
    parts = composite_id.split(":")
    if len(parts) != 2:
        raise ValidationException(detail=(
            "composite task id should be in format of task_type:task_id"
        ))
    task_type, task_id = parts
    if task_type not in {"quiz", "code"}:
        raise ValidationException(detail=(
            "task_type should either be 'quiz' or 'code'"
        ))
    try:
        task_id_int = int(task_id)
    except ValueError as exc:
        raise ValidationException("task_id should be an int") from exc
    return task_type, task_id_int
