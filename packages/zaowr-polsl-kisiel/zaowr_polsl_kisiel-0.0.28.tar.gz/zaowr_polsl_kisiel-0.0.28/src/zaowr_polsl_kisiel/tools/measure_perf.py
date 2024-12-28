import time
from typing import Callable, Any, Optional #, TypeVar
from functools import wraps

# Define a generic type variable for the function
# F = TypeVar("F", bound=Callable[..., Any])

def measure_perf(output_file: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to measure the execution time of a function.

    :param output_file: The path to a file where performance results should be saved.
                        If None, results will only be printed to the console.
    :type output_file: str, optional
    :return: A decorator that logs or saves the execution time of a function.
    :rtype: Callable
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        The inner decorator function.

        :param func: The function to be wrapped and measured.
        :type func: Callable
        :return: The wrapped function.
        :rtype: Callable
        """
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any | None:
            """
            The wrapper function that measures performance.

            :param args: Positional arguments for the wrapped function.
            :param kwargs: Keyword arguments for the wrapped function.
            :return: The result of the wrapped function.
            :rtype: Any
            """
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            message = f"[PERFORMANCE] Function '{func.__name__}' executed in {elapsed_time:.4f} seconds."
            print(message)
            if output_file:
                with open(output_file, "a") as f:
                    f.write(message + "\n")
            return result
        return wrapper
    return decorator
