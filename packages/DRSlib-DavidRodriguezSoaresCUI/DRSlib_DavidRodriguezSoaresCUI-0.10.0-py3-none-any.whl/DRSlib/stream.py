# pylint: disable=broad-except, unnecessary-lambda-assignment
"""
Stream toolbox
==============

Brings Java's Stream syntax to Python for readable functional code use
"""
from collections import defaultdict
import copy
import logging
from dataclasses import dataclass
from functools import partial
from itertools import chain
from typing import Any, Callable, Collection, Iterable, Type

Predicate = Callable[[Any], bool]
IDENTITY = lambda x: x
NULL_CONSUMER = lambda x: None
FILTER_NONE = lambda x: x is None
FILTER_NOT_NONE = lambda x: x is not None
DEFAULTDICT_LIST_SUPPLIER = lambda: defaultdict(list)
LOG = logging.getLogger(__file__)

# Basic accumulators


def list_accumulator(l: list, x: Any) -> list:
    """Accumulator for type list"""
    l.append(x)
    return l


def set_accumulator(s: set, x: Any) -> set:
    """Accumulator for type set"""
    s.add(x)
    return s


def dict_accumulator_unique_key(
    key_mapper: Callable[[Any], Any],
    value_mapper: Callable[[Any], Any],
    d: dict,
    x: Any,
) -> dict:
    """Accumulator for type dict; key must be unique"""
    key = key_mapper(x)
    if key in d:
        raise KeyError(
            f"Trying to insert element {x} in dict but key {key} already exists"
        )
    d[key] = value_mapper(x)
    return d


def defaultdict_list_accumulator(
    key_mapper: Callable[[Any], Any],
    value_mapper: Callable[[Any], Any],
    d: dict,
    x: Any,
) -> dict:
    """Accumulator for type defaultdict[list]"""
    d[key_mapper(x)].append(value_mapper(x))
    return d


# callable takes (a: Collection, b: Any)
ACCUMULATORS: dict[Type[Any], Callable[[Any, Any], Collection]] = {
    list: list_accumulator,
    set: set_accumulator,
    tuple: lambda t, x: t + (x,),
}
# callable takes (a: Collection, b: Collection)
COMBINERS: dict[Type[Any], Callable[[Any, Any], Collection]] = {
    list: lambda a, b: a + b,
    set: lambda a, b: a.union(b),
    tuple: lambda a, b: a + b,
}


@dataclass
class Collector:
    """Describes a component that accepts items and stores them in a collection"""

    supplier: Callable[[], Collection]
    """Supplies a mutable collection to put items in"""
    accumulator: Callable[[Collection, Any], Collection]
    """Adds item in collection"""
    # combiner: Callable
    # """Combine two collections into one"""
    finisher: Callable[[Collection], Any]
    """Applies mapping to collection after adding is done"""

    def collect(self, items: Iterable) -> Collection:
        """Perform collecting"""
        res = self.supplier()
        for item in items:
            res = self.accumulator(res, item)
        return self.finisher(res)

    # static methods

    @staticmethod
    def to_list() -> "Collector":
        """Returns a collector that stores items in a list"""
        return Collector(
            supplier=list, accumulator=ACCUMULATORS[list], finisher=IDENTITY
        )

    @staticmethod
    def to_dict(
        key_mapper: Callable[[Any], Any],
        key_accumulator: Callable[
            [Callable[[Any], Any], Callable[[Any], Any], dict, Any], dict
        ] = dict_accumulator_unique_key,
        value_mapper: Callable[[Any], Any] = IDENTITY,
    ) -> "Collector":
        """Returns a collector that stores items in a dict"""
        return Collector(
            supplier=dict,
            accumulator=partial(key_accumulator, key_mapper, value_mapper),
            finisher=IDENTITY,
        )

    @staticmethod
    def to_defaultdict(
        key_mapper: Callable[[Any], Any],
        value_mapper: Callable[[Any], Any] = IDENTITY,
        defaultdict_collection: Callable[[], Any] = list,
        defaultdict_accumulator: Callable[
            [Callable[[Any], Any], Callable[[Any], Any], dict, Any], dict
        ] = defaultdict_list_accumulator,
    ) -> "Collector":
        """Returns a collector that stores items in a dict"""
        return Collector(
            supplier=lambda: defaultdict(defaultdict_collection),
            accumulator=partial(defaultdict_accumulator, key_mapper, value_mapper),
            finisher=IDENTITY,
        )

    @staticmethod
    def str_join(separator: str = ",") -> "Collector":
        """Returns a collector that stores items (if str, otherwise maps them with str first) in a string"""

        def str_fin(l: Collection) -> str:
            """Concatenates elements with separator"""
            return separator.join(l)

        return Collector(
            supplier=list,
            accumulator=ACCUMULATORS[list],
            finisher=str_fin,
        )


class Stream:
    """Holds elements during processing"""

    input: Collection
    """Contains elements to stream"""

    def __init__(self, of: Iterable) -> None:
        self.input = of if isinstance(of, Collection) else list(of)

    def __str__(self) -> str:
        """Returns a string representation of current state of stream"""
        return f"<Stream: of={self.input} ({type(self.input)})>"

    # static methods
    @staticmethod
    def concat(a: "Stream", b: "Stream") -> "Stream":
        """Creates a new stream that contains all elements from the first stream and
        all the elements of the second stream"""
        return Stream(chain(a.input, b.input))

    # terminal methods

    def all_match(self, predicate: Predicate) -> bool:
        """Returns whether all elements of this stream match the provided predicate."""
        return all(predicate(x) for x in self.input)

    def any_match(self, predicate: Predicate) -> bool:
        """Returns whether all elements of this stream match the provided predicate."""
        return any(predicate(x) for x in self.input)

    def none_match(self, predicate: Predicate) -> bool:
        """Returns whether all elements of this stream match the provided predicate."""
        return not self.any_match(predicate)

    def collect(self, collector: Collector) -> Any:
        """Use collector to store items into a collection"""
        return collector.collect(self.input)

    def count(self) -> int:
        """Count items in stream"""
        return len(self.input)

    def for_each(
        self, consumer: Callable, handle_exceptions: Callable | None = None
    ) -> None:
        """Apply a consumer to each element; terminates the stream"""
        for item in self.input:
            try:
                consumer(item)
            except Exception as e:
                if handle_exceptions is not None:
                    handle_exceptions(e)
                else:
                    raise e
        self.input = []

    def find_first(self) -> Any:
        """Return first item if available, otherwise None"""
        if len(self.input) > 0:
            return self.input[0]
        return None

    def to_list(self) -> Any:
        """Shortcut for .collect(Collector.to_list())"""
        return self.collect(Collector.to_list())

    # non-terminal methods

    def debug(self, logger: Callable | None = None) -> "Stream":
        """logs self to using logger, otherwise to stdout"""
        if logger is None:
            logger = print
        logger(str(self))
        return self

    def distinct(self) -> "Stream":
        """Remove duplicates while keeping order if possible; warning: may be costly on large collections"""
        # short circuit on set because unordered
        if isinstance(self.input, set):
            return self

        # tuple, list (or other)
        res, accumulator = self.__get_collection_and_accumulator()
        known_items: set[Any] = set()
        for item in self.input:
            is_known_item = False
            for known_item in known_items:
                if known_item == item:
                    is_known_item = True
                    break
            if not is_known_item:
                known_items.add(item)
                res = accumulator(res, item)
        self.input = res
        return self

    def unique(self) -> "Stream":
        """Mirror for distinct, for those who prefer that terminology"""
        return self.distinct()

    def filter(self, predicate: Predicate) -> "Stream":
        """Filter out any element that don't match the predicate"""
        res, accumulator = self.__get_collection_and_accumulator()
        for item in self.input:
            if predicate(item):
                res = accumulator(res, item)
        self.input = res
        return self

    def filter_whitelist(self, whitelist: set) -> "Stream":
        """Mirror for filter, for when we want to filter values against a whitelist"""
        return self.filter(lambda x: x in whitelist)

    def filter_blacklist(self, blacklist: set) -> "Stream":
        """Mirror for filter, for when we want to filter values against a blacklist"""
        return self.filter(lambda x: x not in blacklist)

    def map(
        self, mapper: Callable, handle_exceptions: Callable | None = None
    ) -> "Stream":
        """Apply a mapping to each element"""
        res, accumulator = self.__get_collection_and_accumulator()
        for item in self.input:
            try:
                res = accumulator(res, mapper(item))
            except Exception as e:
                if handle_exceptions is not None:
                    handle_exceptions(e)
                else:
                    raise e

        self.input = res
        return self

    def limit(self, max_size: int) -> "Stream":
        """Returns a stream consisting of the elements of this stream,
        truncated to be no longer than max_size in length."""
        if self.count() > max_size:
            res, accumulator = self.__get_collection_and_accumulator()
            for idx, item in enumerate(self.input):
                if idx >= max_size:
                    break
                res = accumulator(res, item)
            self.input = res
        return self

    def skip(self, n: int) -> "Stream":
        """Returns a stream consisting of the elements of this stream,
        truncated to not include the first n elements."""
        if self.count() <= n:
            self.input, _ = self.__get_collection_and_accumulator()
        else:
            res, accumulator = self.__get_collection_and_accumulator()
            for idx, item in enumerate(self.input):
                if idx < n:
                    continue
                res = accumulator(res, item)
            self.input = res
        return self

    def stream_peek(self, stream_action: Callable) -> "Stream":
        """Call stream_action with as input a copy of the items this stream, for example to do some check on the data"""
        stream_action(copy.deepcopy(self.input))
        return self

    # reserved methods

    def __get_collection_and_accumulator(
        self,
    ) -> tuple[Collection, Callable[[Collection, Any], Collection]]:
        """Returns empty collection and accumulator"""
        collection_type = type(self.input)

        # self.input may be a subclass of a collection => switch to base collection
        if collection_type not in ACCUMULATORS:
            for supported_coll_type in ACCUMULATORS:
                if issubclass(collection_type, supported_coll_type):
                    LOG.debug(
                        "Switching collection type to superclass: %s -> %s",
                        collection_type,
                        supported_coll_type,
                    )
                    collection_type = supported_coll_type
                    break
                else:
                    print(f"{collection_type} not a subclass of {supported_coll_type}")
            else:
                raise ValueError(f"Unsupported collection type {collection_type}")

        return collection_type(), ACCUMULATORS[collection_type]


# if __name__ == "__main__":
#     assert Stream((1, 2, 3)).any_match(lambda x: x % 2 == 0) is True
#     assert Stream((1, 2, 3)).all_match(lambda x: x % 2 == 0) is False
#     assert Stream.concat(Stream([1, 2, 3]), Stream(["a", "b", "c"])).collect(
#         Collector.to_list()
#     ) == [1, 2, 3, "a", "b", "c"]
#     assert (
#         Stream((1, 2, 3)).limit(2).count() == 2
#     ), f"count={Stream((1, 2, 3)).limit(2).count()}, res={Stream((1, 2, 3)).limit(2).collect(Collector.to_list())}"
#     assert Stream((1, 2, 3)).limit(2).collect(Collector.to_list()) == [1, 2]
#     assert Stream((1, 2, 3)).limit(3).count() == 3
#     assert Stream((1, 2, 3)).skip(1).count() == 2
#     assert Stream((1, 2, 3)).skip(1).collect(Collector.to_list()) == [2, 3]
#     assert Stream((1, 2, 3)).skip(3).count() == 0
#     assert Stream(["abc", "def", "abc"]).distinct().count() == 2
#     assert Stream(["abc"]).collect(Collector.str_join(" ")) == "abc"
#     assert Stream(["a", "b", "c"]).collect(Collector.str_join(" ")) == "a b c"
