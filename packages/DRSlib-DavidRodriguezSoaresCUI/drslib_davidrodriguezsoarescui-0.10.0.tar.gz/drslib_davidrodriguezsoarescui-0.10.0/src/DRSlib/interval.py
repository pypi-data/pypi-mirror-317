"""
Interval representation implementation
======================================

A simple implementation for generic intervals.
"""
from typing import Optional, Tuple, Union

from .utils import assertTrue

Numerical = Union[float, int]


class InvalidInterval(Exception):
    """Trivial exception for invalid interval"""


class Interval:
    """Represents an interval [a,b] of real (numerical) values
    Note : the interval [a,b] must be strictly positive (a<b)
    """

    # Needed for visibility
    # InvalidInterval = InvalidInterval

    def __init__(
        self, left: Numerical, right: Numerical, boundary: Optional["Interval"] = None
    ) -> None:
        assertTrue(
            left < right,
            "left={}, right={} do not respect rule: left < right",
            left,
            right,
        )
        self.left = left
        self.right = right
        if isinstance(boundary, Interval):
            res = self.intersection(boundary)
            if res is not None:
                self.left, self.right = res

    @property
    def len(self) -> Numerical:
        """Property. Represents the length of the interval"""
        return self.right - self.left

    def __str__(self):
        return f"<Interval {self.left:.2f}-{self.right:.2f} [{self.len:.2f}]>"

    def __iter__(self):
        return iter([self.left, self.right])

    def intersection(
        self, other: "Interval", return_obj: bool = False, raise_exception: bool = True
    ) -> Union["Interval", Tuple[Numerical, Numerical], None]:
        """Computes the intersection between two Interval objects.
        Let [x,y] be the valid strictly interval representing the intersection (only exists on
        strictly overlapping intervals).

        Returns : either an Interval object representing the [x,y] interval (if `return_obj`),
        or the (x,y) tuple (if not `return_obj`), or nothing if [x,y] doesn't exist
        (see `raise_exception` below).

        `raise_exception` : allows to disable raising exception, returning None instead.
        """
        assertTrue(
            isinstance(other, Interval), "Expected Interval, found {}", type(other)
        )
        left = self.left if other.left < self.left else other.left
        right = self.right if self.right < other.right else other.right
        if right <= left and raise_exception:
            # non-strictly overlapping intervals
            raise InvalidInterval()
        # valid intersection exists
        return Interval(left, right) if return_obj else (left, right)

    @classmethod
    def from_length(
        cls,
        length: Numerical,
        start: Optional[Numerical] = None,
        end: Optional[Numerical] = None,
    ) -> "Interval":
        """Creates an Interval from 2 (or more) of an interval's properties : start point, end point, length"""
        assertTrue(0 < length, "Interval must have non-zero lenth")
        if start is not None:
            if end is not None:
                assertTrue(
                    abs((end - start) - length) < (end - start) * 0.01,
                    "argument mismatch",
                )
            else:
                end = start + length
        elif end is not None:
            start = end - length
        return Interval(start, end)  # type: ignore[arg-type]

    def contains(self, x: Numerical, strict: bool = False) -> bool:
        """Returns True if x is in interval, False otherwise"""
        if strict:
            return self.left < x < self.right
        return self.left <= x <= self.right

    @property
    def math_repr(self) -> str:
        """Basic math representation: [<left>,<right>]"""
        return f"[{self.left},{self.right}]"

    def split(self, x: Numerical) -> Tuple["Interval", "Interval"]:
        """Split interval in two. If not possible, raise error"""
        if not self.contains(x, strict=True):
            raise InvalidInterval(
                f"Can't split interval {self.math_repr} using point {x} not strictly in interval."
            )
        return (Interval(self.left, x), Interval(x, self.right))

    def merge(self, other: "Interval") -> "Interval":
        """Return merged interval"""
        if self.right == other.left:
            return Interval(self.left, other.right)
        if self.left == other.right:
            return Interval(other.left, self.right)
        raise InvalidInterval(
            f"Can't merge intervals {self.math_repr} and [{other.left},{other.right}]"
        )
