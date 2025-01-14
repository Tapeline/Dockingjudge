from typing import TypeVar, Annotated

T = TypeVar("T")
type MutatedArgument[T] = Annotated[T, "MutatedArgument"]
