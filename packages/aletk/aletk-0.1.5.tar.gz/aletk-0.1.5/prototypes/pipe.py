### TO DELETE IF THIS EVER GETS IMPLEMENTED IN THE MAIN LIBRARY ###
import sys
sys.path.append('..')
### ###

from typing import Callable

from src.aletk.ResultMonad import Err, Ok

class pipe[T]:
    """
    A pipe object that can be used to chain functions together with the `>>` operator.

    ### Example

    ```python
    from aletk import pipe

    def add_one(x: int) -> int:
        return x + 1

    def multiply_by_two(x: int) -> int:
        return x * 2
    
    result = pipe(1) >> add_one >> multiply_by_two
    print(result.output)  # 4
    ``
    """
    def __init__(self, value: T):
        self.value = value

    @property
    def output(self) -> T:
        return self.value

    def __rshift__[U](
        self, func: Callable[[T | 'pipe[T]'], U | Ok[U]]
    ) -> 'pipe[U]' | U | 'pipe[T]' | Err | 'pipe[Err]' | Ok[U]:
        if func is pipe_out:
            # If the function is `pipe_out`, call it directly on `self`
            return func(self)

        if isinstance(self.value, Err):
            # Propagate Err without calling the function
            return self

        if isinstance(self.value, Ok):
            # Unwrap the Ok value
            unwrapped_value = self.value.out
        else:
            # Regular value
            unwrapped_value = self.value

        # Call the function
        result = func(unwrapped_value)

        if isinstance(result, Err):
            # Propagate Err if returned by the function
            return pipe(result)
        elif isinstance(result, Ok):
            # Wrap Ok result in pipe
            return pipe(result)  # type: ignore
        else:
            # Wrap regular result in pipe
            return pipe(result)

    def __or__[U](self, func: Callable[[T | 'pipe[T]'], U]) -> 'pipe[U]' | U:
        if func is pipe_out:
            return func(self)
        return pipe(func(self.value))

    def __repr__(self) -> str:
        return f'{self.value}'


def pipe_out[T](pipe_result: pipe[T] | pipe[Ok[T]] | T) -> T:
    if isinstance(pipe_result, pipe):
        if isinstance(pipe_result.output, Ok):
            return pipe_result.output.out

        return pipe_result.output  # Return the unwrapped result
    return pipe_result
