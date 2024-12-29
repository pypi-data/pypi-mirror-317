# pylint: disable=too-few-public-methods, abstract-method
"""
Multiprocessing
===============

For when even the most basic parallel processing is
better than nothing
"""
import multiprocessing
from multiprocessing.pool import Pool
from typing import Any, Callable, List, Tuple


MULTIPROCESSING_CONTEXT_TYPE: type = type(multiprocessing.get_context())


class NoDaemonProcess(multiprocessing.Process):
    """Patches Process to not allow deamon processes"""

    @property
    def daemon(self):
        return False

    @daemon.setter
    def daemon(self, value):
        pass


class NoDaemonContext(MULTIPROCESSING_CONTEXT_TYPE):
    """Context that does not allow deamon processes"""

    Process = NoDaemonProcess


# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class NestablePool(Pool):
    """Based on multiprocessing.pool.Pool but allows subprocesses to
    create their own subprocesses, by making them non-deamonic.
    Only appropriate where all parents are waiting for children to finish.
    Use with caution (recursive runaway is very possible)
    Probably inspired from https://stackoverflow.com/a/8963618
    """

    def __init__(self, *args, **kwargs):
        kwargs["context"] = NoDaemonContext()
        super().__init__(*args, **kwargs)


class SimpleMultiProcessing:
    """Parallel processing made simpler
    (!) Since 0.8.0 SimpleMultiProcessing allows for nested multiprocessing. Use carefully !
    """

    @staticmethod
    def apply_kwargs(
        user_function_and_arguments: Tuple[Callable, tuple, dict]
    ) -> Callable:
        """Workaround for imap only taking one argument per thread
        Executes user function with provided arguments"""
        user_function, args, kwargs = user_function_and_arguments
        return user_function(*args, **kwargs)

    @staticmethod
    def bulk_processing(
        user_function: Callable, arguments: List[dict], parallel_instances: int
    ) -> List[Any]:
        """Takes in callable, kwargs arguments for each thread and number of instances
        to execute in parallel at a time. Returns execution's return value in order.
        """
        user_function_and_arguments = [
            (user_function, (), _args) for _args in arguments
        ]
        with NestablePool(parallel_instances) as pool:
            return list(
                pool.imap(
                    SimpleMultiProcessing.apply_kwargs, user_function_and_arguments
                )
            )
