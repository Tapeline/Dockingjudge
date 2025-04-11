from typing import Annotated

type MutatedArgument[T] = Annotated[T, "MutatedArgument"]
