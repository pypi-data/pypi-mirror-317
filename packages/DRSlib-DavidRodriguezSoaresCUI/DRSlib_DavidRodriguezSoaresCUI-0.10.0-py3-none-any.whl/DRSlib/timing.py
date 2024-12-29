import functools
from collections import defaultdict
from time import time
from typing import Any, Callable


class CalledMoreThanOnceException(Exception):
    pass


class TimerIsNotRunningException(Exception):
    pass


class ExecutionTimer:
    """Simplistic way to measure execution time.
    """

    named_timers: dict[str, float]
    """To keep track of execution time for methods"""
    start_time: float
    """Start time for execution"""
    end_time: float
    """End time for execution"""

    TIMER_UNSET = 0.0

    def __init__(self, create_started: bool = False) -> None:
        self.reset(create_started)

    @property
    def active(self) -> bool:
        """Return True if timer is running. Designed to be used with decorator `register_timer` on methods
        to measure more precisely
        """
        return (
            self.start_time is not self.TIMER_UNSET
            and self.end_time is self.TIMER_UNSET
        )

    def reset(self, create_started: bool = False) -> None:
        """Initialize timer"""
        self.named_timers = defaultdict(float)
        self.start_time = self.TIMER_UNSET
        self.end_time = self.TIMER_UNSET
        if create_started:
            self.start()

    def start(self) -> None:
        """Start timer (may only be called once)"""
        if self.start_time is not self.TIMER_UNSET:
            raise CalledMoreThanOnceException(
                "ExecutionTimer.start may not be called more than once"
            )
        self.start_time = time()

    def stop(self) -> None:
        """Stop timer (may only be called once)"""
        if self.end_time is not self.TIMER_UNSET:
            raise CalledMoreThanOnceException(
                "ExecutionTimer.stop may not be called more than once"
            )
        self.end_time = time()

    @property
    def total_execution_time(self) -> float:
        """When the timer has been stopped, returns total time between start() and stop() calls"""
        if self.start_time is self.TIMER_UNSET or self.end_time is self.TIMER_UNSET:
            return 0.0
        return self.end_time - self.start_time

    @property
    def total_named_execution_time(self) -> float:
        """Returns the sum total of execution time for named timers"""
        return sum(self.named_timers.values())

    def resume(self) -> str:
        """Returns a detailed resume of the recorded execution time"""
        # return f"{self.named_timers=} {self.start_time=} {self.end_time=}"
        other_time = self.total_execution_time - self.total_named_execution_time
        return "\n".join(
            ["Execution time:"]
            + [
                f" - {method}: {exec_time:.1f}s"
                for method, exec_time in self.named_timers.items()
            ]
            + [
                f" - Other: {other_time:.1f}s",
                f"TOTAL: {self.total_execution_time:.1f}s",
            ]
        )

    def add_execution_time(
        self, name: str, time_to_add: float, split_from_timers: list[str] | None
    ) -> None:
        """Adds time to a named timer
        `split_from_timers`: used in case timed method B is executed within timed method A. In order for execution time to be accounted for B but not A, it is necessary to set split_from_timers=["A"]
        """
        if not self.active:
            raise TimerIsNotRunningException("Can't add time to inactive timer")
        if time_to_add < 0.0:
            raise ValueError(
                f"Adding time requires the value to be positive but got {time_to_add=} ({name=})"
            )

        self.named_timers[name] += time_to_add

        # remove execution time from other timed methods
        if split_from_timers:
            for name in split_from_timers:
                self.named_timers[name] -= time_to_add


def register_timer(
    time_keeper: ExecutionTimer,
    timer_name: str | None = None,
    split_from_timers: list[str] | None = None,
) -> Callable:
    """Add this decorator to a method to automate execution time keeping
    `split_from_timers`: used in case timed method B is executed within timed method A. In order for execution time to be accounted for B but not A, it is necessary to set argument split_from_timers=["A"]
    """

    def actual_decorator(user_function: Callable) -> Callable:
        # Automatically resolve name using methods name
        nonlocal timer_name

        if timer_name is None:
            timer_name = user_function.__name__

        @functools.wraps(user_function)
        def wrapper(*args, **kwargs) -> Any:
            nonlocal user_function, time_keeper, timer_name, split_from_timers

            t0 = time()
            res = user_function(*args, **kwargs)
            exec_time = time() - t0
            time_keeper.add_execution_time(timer_name, exec_time, split_from_timers)

            return res

        return wrapper

    return actual_decorator
