"""
Dictionnary utils
=================

Methods that perform simple but convenient operations,
specifically on dictionnaries
"""

from typing import Any, Callable, Dict, List, Set

from .utils import assertTrue, cast_number


def flatten_dict_join(d: Dict[str, Any]) -> Dict[str, Any]:
    """Returns a dictionnary with similar content but no nested dictionnary value
    WARNING: requires all keys to be str !
    Strategy to conserve key uniqueness is `key joining`:  d[k1][k2] -> d[k1.k2]
    """
    dflat = {}
    for k, v in d.items():
        assertTrue(isinstance(k, str), "Key {} is a {}, not str !", k, type(k))
        if isinstance(v, dict):
            d2 = flatten_dict_join(v)
            for k2, v2 in d2.items():
                assertTrue(
                    isinstance(k, str), "Key {} is a {}, not str !", k2, type(k2)
                )
                k1_2 = k + "." + k2
                assertTrue(
                    k1_2 not in dflat, "Collision: key {} already in dict !", k1_2
                )
                dflat[k1_2] = v2
            continue

        assertTrue(k not in dflat, "Collision: key {} already in dict !", k)
        dflat[k] = v

    return dflat


def dict_difference(dictA: dict, dictB: dict) -> dict:
    """Performs dictA - dictB on the values: Returns a dictionnary
    with all items from dictA minus the key-value pairs in common with dictB"""
    diff = {
        k: dict_difference(v_a, dictB[k])
        if isinstance(v_a, dict) and k in dictB
        else v_a
        for k, v_a in dictA.items()
        if (k not in dictB) or (isinstance(v_a, dict) or v_a != dictB[k])
    }
    for k in list(diff.keys()):
        if diff[k] == {}:
            del diff[k]
    return diff


def dict_intersection(dicts: List[dict]) -> dict:
    """Given a list of dictionnaries, returns the common elements
    determined by key
    """
    assertTrue(
        len(dicts) > 1, "Expected at least 2 dictionnaries, found {}", len(dicts)
    )
    assertTrue(
        all(d is not None and isinstance(d, dict) for d in dicts),
        "Invalid argument: some items are Nore or not dicts!",
    )

    common = {}

    for k, vref in dicts[0].items():
        if not all(k in d for d in dicts[1:]):
            # Some dicts don't have key `k`
            continue
        if isinstance(vref, dict):
            common_v = dict_intersection([d[k] for d in dicts])
            common[k] = common_v if common_v else "<varies>"
            continue
        value_set = set(d[k] for d in dicts)
        if len(value_set) != 1:
            # Divergent values for key `k`
            common[k] = "<varies>"
            continue
        common[k] = vref

    return common


def dict_list_keys(d: dict) -> List[str]:
    """Searches (recursively) for all keys within dictionnary and returns them in an ordered list.
    Warns on duplicate."""

    def add_item_to_set_or_warn(_set: Set[Any], item: Any) -> None:
        if item in _set:
            print(f"Item '{item}' already in set !")
        else:
            _set.add(item)

    keys: Set[str] = set()
    for k in d:
        if isinstance(d[k], dict):
            for k2 in dict_list_keys(d[k]):
                add_item_to_set_or_warn(keys, k2)
            continue
        add_item_to_set_or_warn(keys, k)

    return list(sorted(keys))


class ChangeDetectDict(dict):
    """Normal dict but has the ability to detect if it was edited since initialization.
    Should be initialised from method from_dict"""

    EDIT_DETECT_FIELD: str = "__edit_detect__"

    def __setitem__(self, __key, __value) -> None:
        """Records that dict was edited"""
        setattr(self, ChangeDetectDict.EDIT_DETECT_FIELD, True)
        super().__setitem__(__key, __value)

    def __delitem__(self, __key) -> None:
        """Records that dict was edited"""
        setattr(self, ChangeDetectDict.EDIT_DETECT_FIELD, True)
        super().__delitem__(__key)

    @property
    def was_edited(self) -> bool:
        """Returns true if dict was edited"""
        return getattr(self, ChangeDetectDict.EDIT_DETECT_FIELD, False)

    @staticmethod
    def from_dict(d: dict) -> "ChangeDetectDict":
        """Creates instance of ChangeDetectDict from dict"""
        instance = ChangeDetectDict(d)
        setattr(instance, ChangeDetectDict.EDIT_DETECT_FIELD, False)
        return instance


def dict_try_casting_values(
    data: dict,
    in_place: bool = False,
    cast_numbers: bool = True,
    cast_bool: dict[str, bool] | None = None,
    external_mapper: Callable[[str], Any] | None = None,
) -> dict:
    """Attempts casting dictionnary values
    `in_place`: True: edit values in place and return input dict; False: return a new dict
    `cast_numbers`: if True, attempts to cast numbers from strings, eg: "-23" (str) -> -23 (int), "3.14" (str) -> 3.14 (float)
    `cast_bool`: allow for casting boolean values given mapping
    `external_mapper`: allow for more advanced mapping (see `str_utils.human_parse_int`)
    """
    if not data:
        return {}

    input_data, output_data = data, data if in_place else {}
    do_cast_bool = cast_bool is not None and len(cast_bool) > 0
    do_external_cast = external_mapper is not None

    def best_effort_casting_str(v: str):
        if cast_numbers:
            _value = cast_number(v)
            if isinstance(_value, (int, float)):
                return _value
        if do_cast_bool and v in cast_bool:  # type: ignore[operator]
            return cast_bool[v]  # type: ignore[index]
        if do_external_cast:
            return external_mapper(v)  # type: ignore[misc]
        return v

    def best_effort_casting(v: Any):
        if isinstance(v, dict):
            return dict_try_casting_values(
                v, in_place, cast_numbers, cast_bool, external_mapper
            )
        if isinstance(v, list):
            return [best_effort_casting(vv) for vv in v]
        if isinstance(v, str):
            return best_effort_casting_str(v)
        return v

    for k, v in input_data.items():
        output_data[k] = best_effort_casting(v)

    return output_data
