"""
General Utils module
====================

A collection of tools that do not fit in other modules.
"""
import collections
import inspect
import logging
import pickle
from pathlib import Path
from typing import Any, Callable, Optional, Self, Tuple, Union

LOG = logging.getLogger(__file__)

LOG_FORMAT_VERBOSE = "[%(levelname)s:%(filename)s:%(lineno)d] %(message)s"
LOG_FORMAT_EXTENDED = "[%(levelname)s:%(funcName)s] %(message)s"
LOG_FORMAT_BASIC = "[%(levelname)s] %(message)s"


def assertTrue(condition: bool, message: str, *arguments) -> None:
    """Like assert, but without its optimization issues"""
    if not condition:
        caller = caller_info()
        raise AssertionError(
            f"[{caller['file'].stem}:{caller['name']}] " + message.format(*arguments)
        )


def caller_info() -> dict:
    """Uses module inspect to retrieve caller info: file, name, line, code"""
    frame = inspect.stack()[2]
    return {
        "file": Path(frame.filename),
        "name": frame.function,
        "line": frame.lineno,
        "code": None
        if frame.code_context is None
        else " ".join(frame.code_context).strip(),
    }


def pickle_this(data: Any, save_file: Path) -> None:
    """Stores `data` to a file"""
    with save_file.open(mode="wb") as fp:  # Pickling
        pickle.dump(data, fp)
        LOG.debug("Successfully stored data to file %s.", save_file)


def unpickle_this(save_file: Path) -> Any:
    """Reads data from a file that was created by `pickle_this`"""
    if not save_file.is_file():
        LOG.debug("Could not find file %s.", save_file)
        return None
    with save_file.open(mode="rb") as fp:  # Unpickling
        LOG.debug("Successfully retrieved data from file %s.", save_file)
        return pickle.load(fp)


def is_iterable(a: Any) -> bool:
    """Checks if object is iterable, thus having attribute `__iter__`.

    Bugfix 2021-11-09: hasattr(a, "__iter__") was true on type str

    Potential future fix: According to collections.abc.Iterable, "The only reliable way to determine whether an object is iterable is to call iter(obj)."
    See method 3 at https://www.geeksforgeeks.org/how-to-check-if-an-object-is-iterable-in-python/
    """
    return isinstance(a, collections.abc.Iterable)


def type_assert(
    v: object,
    v_name: str,
    expected_type: Union[type, Tuple[type]],
    prefix: str,
    accept_none: bool = False,
) -> None:
    """Makes sure a variable is of given type(s).

    Raises AssertionError if `v` has type not covered by `expected_type`.

    `prefix` : A string prefix for the message the raised error may display, useful for knowing which
               part of the code generated the error. eg: 'MyClass.method2'

    `accept_none` : if True, accepts a `None` value for `v` no matter the expected type(s).
                    Alternatively, include `type(None)` to the expected type list.
    """
    # Case 1 : accept None value
    if accept_none is True and v is None:
        return

    error_txt = f"{prefix}: expected received '{v_name}' to be a {expected_type} object, received '{type(v)}'"
    # Case 2 : expected_type is a list/set => recursion
    if is_iterable(expected_type):
        for e_t in expected_type:  # type: ignore
            try:
                type_assert(v, v_name, e_t, prefix, accept_none)
                return
            except AssertionError:
                continue
        raise AssertionError(error_txt)

    # Default case : check type
    assertTrue(isinstance(v, expected_type), error_txt)


def safe_re(
    method: Callable, *args, mapping: Optional[Callable] = None, **kwargs
) -> Optional[Any]:
    """Safely call re method with arguments, and apply mapping to the result.
    Does not raise exception on failure but returns None
    """
    try:
        res = method(*args, **kwargs)
        if res is None:
            return None
        return res if mapping is None else mapping(res)
    except Exception:
        return None


def cast_number(number: str) -> int | float | str:
    """Attempts to cast number to int or float"""
    try:
        return int(number)
    except ValueError:
        try:
            return float(number)
        except ValueError:
            return number


class Singleton(type):
    """For when a class requires a single instance to exist at any time
    usage: class MyClass(BaseClass, metaclass=Singleton): ...
    Code from https://stackoverflow.com/questions/6760685/what-is-the-best-way-of-implementing-singleton-in-python
    """

    _instances = {}

    @classmethod
    def __call__(cls, *args, **kwargs) -> Self:
        """Returns instance if exists or creates a new one"""
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
